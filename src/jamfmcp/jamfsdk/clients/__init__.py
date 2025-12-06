import asyncio
import logging
import tempfile
from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    Callable,
    Iterable,
    Iterator,
)
from urllib.parse import urlunparse

import certifi
import httpx
from pydantic import BaseModel

from ..clients.classic_api import ClassicApi
from ..clients.jcds2 import JCDS2
from ..clients.pro_api import ProApi
from ..models.classic import ClassicApiModel
from ..models.client import SessionConfig
from .auth import CredentialsProvider

logger = logging.getLogger("jamfsdk")


class JamfProClient:
    def __init__(
        self,
        server: str,
        credentials: CredentialsProvider,
        port: int = 443,
        session_config: SessionConfig | None = None,
    ):
        """
        The base client class for interacting with the Jamf Pro APIs.

        Classic API, Pro API, and JCDS2 clients are instantiated with the base client.

        If the ``aws`` extra dependency is not installed the JCDS2 client will not be created.

        :param server: The hostname of the Jamf Pro server to connect to.
        :type server: str

        :param credentials: Accepts any credentials provider object to provide the
            username and password for initial authentication.
        :type credentials: CredentialsProvider

        :param port: The server port to connect over (defaults to `443`).
        :type port: int

        :param session_config: Pass a `SessionConfig` to configure session options.
        :type session_config: SessionConfig
        """
        self.session_config = SessionConfig() if not session_config else session_config

        self._credentials = credentials
        self._credentials.attach_client(self)
        self.get_access_token = self._credentials.get_access_token

        self.base_server_url = urlunparse(
            (
                self.session_config.scheme,
                f"{server}:{port}",
                "",
                None,
                None,
                None,
            )
        )

        self._session = None
        self._session_semaphore = asyncio.Semaphore(self.session_config.max_concurrency)

        self.classic_api = ClassicApi(self.classic_api_request, self.concurrent_api_requests)
        self.pro_api = ProApi(self.pro_api_request, self.concurrent_api_requests)

        try:
            self.jcds2 = JCDS2(self.classic_api, self.pro_api, self.concurrent_api_requests)
        except ImportError:
            pass

    @staticmethod
    def _parse_cookie_file(cookie_file: str | Path) -> dict[str, str]:
        """Parse a cookies file and return a dictionary of key value pairs."""
        cookies = {}
        with open(cookie_file, "r") as fp:
            for line in fp:
                if line.startswith("#HttpOnly_"):
                    fields = line.strip().split()
                    cookies[fields[5]] = fields[6]
        return cookies

    @staticmethod
    def _load_ca_cert_bundle(ca_cert_bundle_path: str | Path):
        """
        Create a copy of the certifi trust store and append the passed CA cert bundle in a
        temporary file.
        """
        with open(certifi.where(), "r") as f_obj:
            current_ca_cert = f_obj.read()

        with open(ca_cert_bundle_path, "r") as f_obj:
            ca_cert_bundle = f_obj.read()

        temp_ca_cert_dir = tempfile.mkdtemp(prefix="jamf-pro-sdk-")
        temp_ca_cert = f"{temp_ca_cert_dir}/cacert.pem"

        with open(temp_ca_cert, "w") as f_obj:
            f_obj.write(current_ca_cert)
            f_obj.write(ca_cert_bundle)

        return temp_ca_cert

    async def _get_session(self) -> httpx.AsyncClient:
        """
        Get or create an httpx AsyncClient.

        :return: An httpx AsyncClient instance.
        :rtype: httpx.AsyncClient
        """
        async with self._session_semaphore:
            if self._session is None or self._session.is_closed:
                # Setup SSL context
                ssl_context = None
                if self.session_config.ca_cert_bundle is not None:
                    import ssl

                    ssl_context = ssl.create_default_context(cafile=certifi.where())
                    ssl_context.load_verify_locations(cafile=self.session_config.ca_cert_bundle)
                elif not self.session_config.verify:
                    import ssl

                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE

                # Setup timeout
                timeout = (
                    httpx.Timeout(self.session_config.timeout)
                    if self.session_config.timeout
                    else None
                )

                # Setup limits
                limits = httpx.Limits(
                    max_connections=self.session_config.max_concurrency,
                    max_keepalive_connections=self.session_config.max_concurrency,
                )

                # Setup headers
                headers = {
                    "Accept": "application/json",
                    "User-Agent": self.session_config.user_agent,
                }

                # Setup cookies
                cookies = None
                if self.session_config.cookie:
                    cookies = self._parse_cookie_file(self.session_config.cookie)

                # Setup verify parameter for SSL
                verify = ssl_context if ssl_context else self.session_config.verify

                self._session = httpx.AsyncClient(
                    limits=limits,
                    timeout=timeout,
                    headers=headers,
                    cookies=cookies,
                    verify=verify,
                )

            return self._session

    @staticmethod
    async def parse_json_response(response: httpx.Response) -> dict:
        """
        Parse JSON response, ignoring Content-Type header.

        This utility method works around servers that return valid JSON
        with incorrect Content-Type headers (e.g., text/plain instead of application/json).

        :param response: The httpx Response object
        :type response: httpx.Response
        :return: Parsed JSON data
        :rtype: dict
        """
        return response.json()

    async def close(self) -> None:
        """
        Close the httpx session.
        """
        if self._session and not self._session.is_closed:
            await self._session.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def classic_api_request(
        self,
        method: str,
        resource_path: str,
        data: str | ClassicApiModel | None = None,
        override_headers: dict | None = None,
    ) -> httpx.Response:
        """
        Perform a request to the Classic API.

        :param method: The HTTP method. Allowed values (case-insensitive) are: GET, POST,
            PUT, and DELETE.
        :type method: str

        :param resource_path: The path of the API being requested that comes `after`
            ``JSSResource``.
        :type resource_path: str

        :param data: If the request is a ``POST`` or ``PUT``, the XML string or
            ``ClassicApiModel`` that is being sent.
        :type data: str | ClassicApiModel

        :param override_headers: A dictionary of key-value pairs that will be set as
            headers for the request. You cannot override the ``Authorization`` or
            ``Content-Type`` headers.
        :type override_headers: dict[str, str]

        :return: `httpx Response <https://www.python-httpx.org/api/#response>`_ object
        :rtype: httpx.Response
        """
        session = await self._get_session()
        url = f"{self.base_server_url}/JSSResource/{resource_path}"

        headers = {
            "Authorization": f"Bearer {await self._credentials.get_access_token()}",
            "Content-Type": "application/json",
        }

        if override_headers:
            headers.update(override_headers)

        content = None
        if data and (method.lower() in ("post", "put")):
            headers["Content-Type"] = "text/xml"
            content = data if isinstance(data, str) else data.xml(exclude_read_only=True)

        logger.info("ClassicAPIRequest %s %s", method.upper(), resource_path)

        try:
            capi_resp = await session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                content=content,
            )
            capi_resp.raise_for_status()
        except httpx.HTTPStatusError:
            # TODO: XML error response parser
            error_text = capi_resp.text
            logger.error(error_text)
            raise

        return capi_resp

    async def pro_api_request(
        self,
        method: str,
        resource_path: str,
        query_params: dict[str, str] | None = None,
        data: dict | BaseModel | None = None,
        files: dict[str, tuple[str, BinaryIO, str]] | None = None,
        override_headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """
        Perform a request to the Pro API.

        :param method: The HTTP method. Allowed values (case-insensitive) are: GET, POST,
            PUT, PATCH, and DELETE.
        :type method: str

        :param resource_path: The path of the API being requested that comes `after`
            ``api``. Include the API version at the beginning of the resource path.
        :type resource_path: str

        :param query_params: Query string parameters to be included with the request URL string.
        :type query_params: dict[str, str]

        :param data: If the request is a ``POST``, ``PUT``, or ``PATCH``, the dictionary
            or ``BaseModel`` that is being sent.
        :type data: dict | BaseModel | None

        :param files: If the request is a ``POST``, a dictionary with a single ``files`` key,
            and a tuple containing the filename, file-like object to upload, and mime type.
        :type files: dict[str, tuple[str, BinaryIO, str]] | None

        :param override_headers: A dictionary of key-value pairs that will be set as
            headers for the request. You cannot override the ``Authorization`` or
            ``Content-Type`` headers.
        :type override_headers: dict[str, str]

        :return: `httpx Response <https://www.python-httpx.org/api/#response>`_ object
        :rtype: httpx.Response
        """
        session = await self._get_session()
        url = f"{self.base_server_url}/api/{resource_path}"

        headers = {
            "Authorization": f"Bearer {await self._credentials.get_access_token()}",
            "Content-Type": "application/json",
        }

        if override_headers:
            headers.update(override_headers)

        kwargs = {
            "method": method.upper(),
            "url": url,
            "headers": headers,
        }

        if query_params:
            kwargs["params"] = query_params

        if data and (method.lower() in ("post", "put", "patch")):
            headers["Content-Type"] = "application/json"
            if isinstance(data, dict):
                kwargs["json"] = data
            elif isinstance(data, BaseModel):
                kwargs["content"] = data.model_dump_json(exclude_none=True)
            else:
                raise ValueError("'data' must be one of 'dict' or 'BaseModel'")

        if files and (method.lower() == "post"):
            # Convert files to httpx format
            # httpx expects files as a list of tuples
            httpx_files = []
            for field_name, (filename, file_obj, content_type) in files.items():
                httpx_files.append((field_name, (filename, file_obj, content_type)))
            kwargs["files"] = httpx_files
            # Remove Content-Type header when uploading files
            headers.pop("Content-Type", None)

        logger.info("ProAPIRequest %s %s", method.upper(), resource_path)

        pro_resp = await session.request(**kwargs)
        try:
            pro_resp.raise_for_status()
        except httpx.HTTPStatusError:
            error_text = pro_resp.text
            logger.error(error_text)
            raise

        return pro_resp

    async def concurrent_api_requests(
        self,
        handler: Callable,
        arguments: Iterable[Any],
        return_model: type[BaseModel] | None = None,
        max_concurrency: int | None = None,
        return_exceptions: bool | None = None,
    ) -> Iterator[Any | Exception]:
        """
        An interface for performing concurrent API operations.

        :param handler: The method that will be called.
        :type handler: Callable

        :param arguments: An iterable object containing the arguments to be passed to the
            ``handler``. If the items within the iterable are dictionaries (``dict``) they
            will be unpacked when passed. Use this to pass multiple arguments.
        :type arguments: Iterable[Any]

        :param return_model: The Pydantic model that should be instantiated from the responses. The
            model will only be returned if the response from the ``handler`` is not also a model. If
            it is the ``return_model`` is ignored. The response MUST be a JSON body for this option
            to succeed.
        :type return_model: BaseModel

        :param max_concurrency: An override the value for ``session_config.max_concurrency``. Note:
            this override `cannot` be higher than ``session_config.max_concurrency``.
        :type max_concurrency: int

        :param return_exceptions: If an exception is encountered by the ``handler`` the
            iterator will continue without a yield. Setting this to ``True`` will return the
            exception object. If not set, the value for ``session_config.return_exceptions`` is
            used.
        :type return_exceptions: bool

        :return: An iterator that will yield the result for each operation.
        :rtype: Iterator
        """
        if return_exceptions is None:
            return_exceptions = self.session_config.return_exceptions

        if max_concurrency:
            max_concurrency = min(max_concurrency, self.session_config.max_concurrency)
        else:
            max_concurrency = self.session_config.max_concurrency

        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrency)

        async def _execute_with_semaphore(arg):
            async with semaphore:
                if isinstance(arg, dict):
                    return await handler(**arg)
                else:
                    return await handler(arg)

        logger.info("ConcurrentAPIRequest %s", handler.__name__)

        # Create tasks for all arguments
        tasks = [_execute_with_semaphore(arg) for arg in arguments]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=return_exceptions)

        for result in results:
            try:
                if isinstance(result, Exception):
                    if return_exceptions:
                        yield result
                    else:
                        logger.warning(result)
                        continue

                if isinstance(result, BaseModel):
                    yield result
                elif isinstance(result, httpx.Response) and return_model:
                    response_json = result.json()
                    response_data = (
                        response_json[return_model._xml_root_name]
                        if hasattr(return_model, "_xml_root_name")
                        else response_json
                    )
                    yield return_model.model_validate(response_data)
                else:
                    yield result
            except Exception as err:
                logger.warning(err)
                if return_exceptions:
                    yield err
                else:
                    continue
