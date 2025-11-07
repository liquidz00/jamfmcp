import asyncio
import logging
from datetime import datetime, timedelta, timezone
from getpass import getpass
from typing import TYPE_CHECKING, Optional, Type, overload

try:
    import keyring
except ImportError:
    KEYRING_IS_INSTALLED = False
    keyring = None
else:
    KEYRING_IS_INSTALLED = True

import httpx

if TYPE_CHECKING:
    from . import JamfProClient

from ..exceptions import CredentialsError
from ..models.client import AccessToken

logger = logging.getLogger("jamfsdk")


class CredentialsProvider:
    """The base credentials provider class all other providers should inherit from."""

    def __init__(self):
        self._client: Optional["JamfProClient"] = None
        self._global_lock = asyncio.Semaphore(1)
        self._access_token = AccessToken()

    def attach_client(self, client: "JamfProClient"):
        self._client = client

    async def get_access_token(self, semaphore: Optional[asyncio.Semaphore] = None) -> AccessToken:
        """
        Thread safe method for obtaining the current API access token.

        :param semaphore: Optional semaphore for controlling access concurrency.
        :type semaphore: Optional[asyncio.Semaphore]

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        if not semaphore:
            semaphore = self._global_lock

        async with semaphore:
            await self._refresh_access_token()
            return self._access_token

    async def _request_access_token(self) -> AccessToken:
        """
        This internal method requests a new Jamf Pro access token.

        Custom credentials providers should override this method. Refer to the ``ApiClientProvider``
        and ``UserCredentialsProvider`` classes for example implementations.

        This method must always return an :class:`~jamfsdk.models.client.AccessToken` object.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        return AccessToken()

    async def _keep_alive(self) -> AccessToken:
        """
        Refresh an access token using the ``keep-alive`` endpoint.

        As of Jamf Pro 10.49 this is only supported by user bearer tokens.

        This method may be removed in a future update.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        logger.debug("Refreshing access token with 'keep-alive'")
        try:
            session = await self._client._get_session()
            url = f"{self._client.base_server_url}/api/v1/auth/keep-alive"
            headers = {
                "Authorization": f"Bearer {self._access_token.token}",
                "Accept": "application/json",
            }

            resp = await session.post(url, headers=headers)
            resp.raise_for_status()
            response_json = resp.json()
            return AccessToken(type="user", **response_json)
        except httpx.HTTPStatusError as err:
            logger.error(err)
            error_text = err.response.text
            logger.debug(error_text)
            raise

    async def _refresh_access_token(self) -> None:
        """
        Requests and stores an API access token.

        Refresh behavior is determined by the token's type.

        For user bearer tokens, if the cached token's remaining time is greater than or equal to 60
        seconds it will be returned. If the cached token's remaining time is greater than 5 seconds
        but less than 60 seconds the token will be refreshed using the ``keep-alive`` API.

        For OAuth tokens, if the cached token's remaining time is greater than or equal to 3 seconds
        it will be returned.

        If the above conditions are not met a new token will be requested.
        """
        if self._client is None:
            raise CredentialsError("A Jamf Pro client is not attached to this credentials provider")

        # TODO: Future OAuth flows may need to set different TTL values for refresh behavior
        token_cache_ttl = 60 if self._access_token.type == "user" else 3

        # Return the cached token if expiration is below the cache TTL
        if (
            self._access_token.token
            and not self._access_token.is_expired
            and self._access_token.seconds_remaining >= token_cache_ttl
        ):
            logger.debug(
                "Using cached access token (%ds remaining)",
                self._access_token.seconds_remaining,
            )
            self._access_token = self._access_token
        # Refresh the cached user bearer token using 'keep-alive'
        elif (
            self._access_token.token
            and self._access_token.type == "user"
            and not self._access_token.is_expired
            and 5 < self._access_token.seconds_remaining < token_cache_ttl
        ):
            self._access_token = await self._keep_alive()
        # Request a new token
        else:
            self._access_token = await self._request_access_token()


class ApiClientCredentialsProvider(CredentialsProvider):
    def __init__(self, client_id: str, client_secret: str):
        """
        A credentials provider that uses OAuth2 client credentials flow using an API client.

        :param client_id: The client ID.
        :type client_id: str

        :param client_secret: The client secret.
        :type client_secret: str
        """
        self.client_id = client_id
        self.client_secret = client_secret
        super().__init__()

    async def _request_access_token(self) -> AccessToken:
        """
        Request a new an API access token using client credentials flow.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        session = await self._client._get_session()
        url = f"{self._client.base_server_url}/api/oauth/token"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        try:
            logger.debug(
                "Requesting new access token (%ds remaining)",
                self._access_token.seconds_remaining,
            )
            resp = await session.post(url, headers=headers, data=data)
            resp.raise_for_status()
        except httpx.HTTPStatusError as err:
            logger.error(err)
            error_text = err.response.text
            logger.debug(error_text)
            raise

        resp_content = resp.content
        logger.debug(resp_content)
        resp_data = resp.json()
        return AccessToken(
            type="oauth",
            token=resp_data["access_token"],
            expires=datetime.now(timezone.utc) + timedelta(seconds=resp_data["expires_in"]),
            scope=resp_data["scope"].split(),
        )


class UserCredentialsProvider(CredentialsProvider):
    def __init__(self, username: str, password: str):
        """
        Credentials provider that uses a username and password for obtaining access
        tokens.

        :param username: The Jamf Pro API username.
        :type username: str

        :param password: The Jamf Pro API password.
        :type password: str
        """
        self.username = username
        self.password = password
        super().__init__()

    async def _request_access_token(self) -> AccessToken:
        """
        Request a new an API access token using user authentication.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        session = await self._client._get_session()
        url = f"{self._client.base_server_url}/api/v1/auth/token"
        headers = {"Accept": "application/json"}
        auth = (self.username, self.password)

        try:
            logger.debug(
                "Requesting new access token (%ds remaining)",
                self._access_token.seconds_remaining,
            )
            resp = await session.post(url, headers=headers, auth=auth)
            resp.raise_for_status()
        except httpx.HTTPStatusError as err:
            logger.error(err)
            error_text = err.response.text
            logger.debug(error_text)
            raise

        response_json = resp.json()
        return AccessToken(type="user", **response_json)


@overload
def prompt_for_credentials(
    provider_type: Type[UserCredentialsProvider],
) -> UserCredentialsProvider: ...


@overload
def prompt_for_credentials(
    provider_type: Type[ApiClientCredentialsProvider],
) -> ApiClientCredentialsProvider: ...


def prompt_for_credentials(
    provider_type: Type[CredentialsProvider],
) -> CredentialsProvider:
    """
    Prompts the user for credentials based on the given provider type.

    Supports both user credentials (username/password) and API client credentials
    (client_id/client_secret), prompting interactively as needed.

    :param provider_type: The credentials provider class to instantiate.
    :type provider_type: Type[CredentialsProvider]
    :return: The ``CredentialsProvider`` object.
    :rtype: CredentialsProvider
    """
    if issubclass(provider_type, UserCredentialsProvider):
        username = input("Jamf Pro Username: ")
        password = getpass("Jamf Pro Password: ")
        return provider_type(username, password)
    elif issubclass(provider_type, ApiClientCredentialsProvider):
        client_id = input("API Client ID: ")
        client_secret = getpass("API Client Secret: ")
        return provider_type(client_id, client_secret)
    else:
        raise TypeError(f"Unsupported credentials provider: {provider_type}")


@overload
def load_from_keychain(
    provider_type: Type[UserCredentialsProvider],
    server: str,
    *,
    username: str,
    client_id: None = None,
) -> UserCredentialsProvider: ...


@overload
def load_from_keychain(
    provider_type: Type[ApiClientCredentialsProvider],
    server: str,
    *,
    client_id: str,
    username: None = None,
) -> ApiClientCredentialsProvider: ...


def load_from_keychain(
    provider_type: Type[CredentialsProvider],
    server: str,
    client_id: Optional[str] = None,
    username: Optional[str] = None,
) -> CredentialsProvider:
    """
    Load credentials from the macOS login keychain and return an instance of the
    specified credentials provider.

    .. important::

        This credentials provider requires the ``macOS`` extra dependency.

    The Jamf Pro API password or client credentials are stored in the keychain with
    the ``service_name`` set to the Jamf Pro server name.

    Supports:
        - ``UserCredentialsProvider``: Retrieves a password using the provided ``username``.
        - ``ApiClientCredentialsProvider``: Retrieves the API client secret using the provided ``client_id``.

    :param provider_type: The credentials provider class to instantiate
    :type provider_type: Type[CredentialsProvider]

    :param server: The Jamf Pro server name.
    :type server: str

    :param client_id: The client ID used for ``ApiClientCredentialsProvider``. Required if ``provider_type`` is that provider.
    :type client_id: Optional[str]

    :param username: The username used for ``UserCredentialsProvider``. Required if ``provider_type`` is that provider.
    :type username: Optional[str]

    :return: An instantiated credentials provider using the keychain values.
    :rtype: CredentialsProvider
    """
    if not KEYRING_IS_INSTALLED:
        raise ImportError("The 'macOS' extra dependency is required.")

    if server.startswith("http://"):
        server = "https://" + server[len("http://") :]
    elif not server.startswith("https://"):
        server = f"https://{server}"

    if issubclass(provider_type, UserCredentialsProvider):
        if username is None:
            raise ValueError(
                "Username argument is required to create UserCredentialsProvider object."
            )
        identity = username
    elif issubclass(provider_type, ApiClientCredentialsProvider):
        if client_id is None:
            raise ValueError(
                "API Client ID is required to instantiate ApiClientCredentialsProvider."
            )
        identity = client_id
    else:
        raise TypeError(f"Unsupported credentials provider: {provider_type}")

    password = keyring.get_password(service_name=server, username=identity)
    if password is None:
        raise CredentialsError(f"Password not found for server {server} and username {identity}")

    return provider_type(identity, password)
