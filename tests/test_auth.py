"""
Simple authentication tests for JamfAuth.
"""

import pytest
from pytest_mock import MockerFixture

from jamfmcp.auth import JamfAuth
from jamfmcp.jamfsdk import ApiClientCredentialsProvider


class TestAuth:
    """Basic authentication tests."""

    def test_client_credentials_auth_creation(self, monkeypatch: MockerFixture) -> None:
        """Test creating OAuth auth with client credentials."""
        monkeypatch.setenv("JAMF_URL", "test.jamfcloud.com")
        monkeypatch.setenv("JAMF_CLIENT_ID", "test-client-id")
        monkeypatch.setenv("JAMF_CLIENT_SECRET", "test-client-secret")

        auth = JamfAuth()

        assert auth.server == "test.jamfcloud.com"
        assert auth.client_id == "test-client-id"
        assert auth.client_secret == "test-client-secret"

        provider = auth.get_credentials_provider()
        assert isinstance(provider, ApiClientCredentialsProvider)

    def test_url_parsing(self) -> None:
        """Test that URLs are parsed to FQDN only."""
        auth = JamfAuth(server="https://test.jamfcloud.com", client_id="test", client_secret="test")

        # Should strip protocol
        assert auth.server == "test.jamfcloud.com"

    def test_missing_url_raises_error(self, monkeypatch: MockerFixture) -> None:
        """Test that missing URL raises appropriate error."""
        monkeypatch.delenv("JAMF_URL", raising=False)

        with pytest.raises(ValueError, match="Jamf Pro server URL not provided"):
            JamfAuth()
