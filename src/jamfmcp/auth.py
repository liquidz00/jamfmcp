import os
from urllib.parse import urlparse

from jamfmcp.jamfsdk import ApiClientCredentialsProvider, UserCredentialsProvider


class JamfAuth:
    """
    Handles authentication for Jamf Pro API.

    Supports both Basic Authentication (username/password) and
    Client Credentials (OAuth) authentication methods.
    """

    def __init__(
        self,
        auth_type: str | None = None,
        server: str | None = None,
        username: str | None = None,
        password: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        """
        Initialize Jamf authentication.

        Parameters can be provided directly or will be read from environment variables:
        - JAMF_AUTH_TYPE: "basic" or "client_credentials" (default: "basic")
        - JAMF_URL: Jamf Pro server URL
        - JAMF_USERNAME: Username for basic auth
        - JAMF_PASSWORD: Password for basic auth
        - JAMF_CLIENT_ID: Client ID for OAuth
        - JAMF_CLIENT_SECRET: Client secret for OAuth

        :param auth_type: Authentication type ("basic" or "client_credentials")
        :param server: Jamf Pro server URL
        :param username: Username for basic auth
        :param password: Password for basic auth
        :param client_id: Client ID for OAuth
        :param client_secret: Client secret for OAuth
        :raises ValueError: If required credentials are missing
        """
        self.auth_type = (auth_type or os.getenv("JAMF_AUTH_TYPE", "basic")).strip().lower()

        raw_server = server or os.getenv("JAMF_URL")
        if not raw_server:
            raise ValueError("Jamf Pro server URL not provided. Set JAMF_URL environment variable.")
        self.server = self._parse_server_url(raw_server)

        if self.auth_type == "basic":
            self.username = username or os.getenv("JAMF_USERNAME")
            self.password = password or os.getenv("JAMF_PASSWORD")
        elif self.auth_type == "client_credentials":
            self.client_id = client_id or os.getenv("JAMF_CLIENT_ID")
            self.client_secret = client_secret or os.getenv("JAMF_CLIENT_SECRET")
        else:
            raise ValueError(
                f"Invalid auth type: {self.auth_type}. Must be 'basic' or 'client_credentials'."
            )

        # init provider
        self._provider = self._create_provider()

    def _create_provider(self) -> UserCredentialsProvider | ApiClientCredentialsProvider:
        """
        Create the appropriate credentials provider based on auth type.

        :return: Configured credentials provider instance
        :rtype: UserCredentialsProvider | ApiClientCredentialsProvider
        :raises ValueError: If required credentials are missing for the auth type
        """
        if self.auth_type == "basic":
            if not self.username or not self.password:
                raise ValueError(
                    "Basic auth credentials not provided. "
                    "Set JAMF_USERNAME and JAMF_PASSWORD environment variables."
                )
            return UserCredentialsProvider(self.username, self.password)

        elif self.auth_type == "client_credentials":
            if not self.client_id or not self.client_secret:
                raise ValueError(
                    "Client credentials not provided. "
                    "Set JAMF_CLIENT_ID and JAMF_CLIENT_SECRET environment variables."
                )
            return ApiClientCredentialsProvider(self.client_id, self.client_secret)

        # Raise value error for anything else
        raise ValueError(f"Unsupported auth_type provided: {self.auth_type}")

    @staticmethod
    def _parse_server_url(url: str) -> str:
        """
        Parse the Jamf URL to ensure it's in the correct format.

        The jamf-pro-sdk expectes the server parameter to be the FQDN,
        not a full URL.

        :param url: The URL to parse
        :type url: str
        :return: The FQDN or netloc portion of the URL
        :rtype: str
        """
        if not url:
            return ""

        url = url.strip()  # Remove leading/trailing whitespace

        if not url.startswith(("http://", "https://")):
            # If no protocol, assume it's already just the domain
            return url

        parsed = urlparse(url)
        return parsed.netloc or parsed.path

    def get_credentials_provider(self) -> UserCredentialsProvider | ApiClientCredentialsProvider:
        """
        Get the credentials provider for the Jamf Pro SDK.

        :return: Configured credentials provider instance
        :rtype: UserCredentialsProvider | ApiClientCredentialsProvider
        """
        return self._provider
