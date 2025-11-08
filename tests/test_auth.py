"""
Simple authentication tests for JamfAuth.
"""

import pytest
from pytest_mock import MockerFixture

from jamfmcp.auth import JamfAuth
from jamfmcp.jamfsdk import ApiClientCredentialsProvider, UserCredentialsProvider


class TestAuth:
    """Basic authentication tests."""

    def test_basic_auth_creation(self, monkeypatch: MockerFixture) -> None:
        """Test creating basic auth with username/password."""
        monkeypatch.setenv("JAMF_URL", "test.jamfcloud.com")
        monkeypatch.setenv("JAMF_USERNAME", "testuser")
        monkeypatch.setenv("JAMF_PASSWORD", "testpass")
        monkeypatch.setenv("JAMF_AUTH_TYPE", "basic")

        auth = JamfAuth()

        assert auth.auth_type == "basic"
        assert auth.server == "test.jamfcloud.com"
        assert auth.username == "testuser"
        assert auth.password == "testpass"

        provider = auth.get_credentials_provider()
        assert isinstance(provider, UserCredentialsProvider)

    def test_client_credentials_auth_creation(self, monkeypatch: MockerFixture) -> None:
        """Test creating OAuth auth with client credentials."""
        monkeypatch.setenv("JAMF_URL", "test.jamfcloud.com")
        monkeypatch.setenv("JAMF_CLIENT_ID", "test-client-id")
        monkeypatch.setenv("JAMF_CLIENT_SECRET", "test-client-secret")
        monkeypatch.setenv("JAMF_AUTH_TYPE", "client_credentials")

        auth = JamfAuth()

        assert auth.auth_type == "client_credentials"
        assert auth.server == "test.jamfcloud.com"
        assert auth.client_id == "test-client-id"
        assert auth.client_secret == "test-client-secret"

        provider = auth.get_credentials_provider()
        assert isinstance(provider, ApiClientCredentialsProvider)

    def test_url_parsing(self) -> None:
        """Test that URLs are parsed to FQDN only."""
        auth = JamfAuth(
            server="https://test.jamfcloud.com", auth_type="basic", username="test", password="test"
        )

        # Should strip protocol
        assert auth.server == "test.jamfcloud.com"

    def test_missing_url_raises_error(self, monkeypatch: MockerFixture) -> None:
        """Test that missing URL raises appropriate error."""
        monkeypatch.delenv("JAMF_URL", raising=False)

        with pytest.raises(ValueError, match="Jamf Pro server URL not provided"):
            JamfAuth()
