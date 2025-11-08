"""
Pytest configuration and shared fixtures.
"""

from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_jamf_env_vars(monkeypatch):
    """
    Automatically set required Jamf environment variables for all tests.

    This prevents import errors when modules try to initialize JamfAuth.
    """
    monkeypatch.setenv("JAMF_URL", "https://test.jamfcloud.com")
    monkeypatch.setenv("JAMF_USERNAME", "test_user")
    monkeypatch.setenv("JAMF_PASSWORD", "test_pass")
    monkeypatch.setenv("JAMF_AUTH_TYPE", "basic")


@pytest.fixture
def mock_jamf_api(mocker: MockerFixture) -> MagicMock:
    """
    Create a mock JamfApi instance.

    :param mocker: Pytest mock fixture
    :type mocker: MockerFixture
    :return: Mock JamfApi instance
    :rtype: MagicMock
    """
    mock_api = mocker.MagicMock()
    mock_api.server = "test.jamfcloud.com"
    return mock_api


@pytest.fixture
def mock_health_analyzer(mocker: MockerFixture) -> MagicMock:
    """
    Create a mock HealthAnalyzer instance.

    :param mocker: Pytest mock fixture
    :type mocker: MockerFixture
    :return: Mock HealthAnalyzer instance
    :rtype: MagicMock
    """
    mock_analyzer = mocker.MagicMock()
    return mock_analyzer
