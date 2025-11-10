"""
Unit tests for the JamfMCP CLI.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from asyncclick.testing import CliRunner
from pytest_mock import MockerFixture

from jamfmcp.cli import (
    check_fastmcp_installed,
    check_uv_installed,
    cli,
    validate_jamf_connection,
)


class TestHelperFunctions:
    """
    Tests for CLI helper functions.
    """

    def test_check_fastmcp_installed_success(self, mocker: MockerFixture) -> None:
        """
        Test checking if FastMCP is installed when it is.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0)

        result = check_fastmcp_installed()

        assert result is True
        mock_run.assert_called_once_with(["fastmcp", "--version"], capture_output=True, text=True)

    def test_check_fastmcp_installed_not_found(self, mocker: MockerFixture) -> None:
        """
        Test checking if FastMCP is installed when it's not.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = FileNotFoundError()

        result = check_fastmcp_installed()

        assert result is False

    def test_check_uv_installed_success(self, mocker: MockerFixture) -> None:
        """
        Test checking if uv is installed when it is.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0)

        result = check_uv_installed()

        assert result is True
        mock_run.assert_called_once_with(["uv", "--version"], capture_output=True, text=True)

    def test_check_uv_installed_not_found(self, mocker: MockerFixture) -> None:
        """
        Test checking if uv is installed when it's not.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = FileNotFoundError()

        result = check_uv_installed()

        assert result is False

    @pytest.mark.asyncio
    async def test_validate_jamf_connection_basic_success(self, mocker: MockerFixture) -> None:
        """
        Test successful Jamf connection validation with basic auth.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock JamfAuth
        mock_auth = mocker.patch("jamfmcp.cli.JamfAuth")
        mock_auth_instance = MagicMock()
        mock_auth.return_value = mock_auth_instance
        mock_auth_instance.server = "https://example.jamfcloud.com"
        mock_auth_instance.get_credentials_provider.return_value = MagicMock()

        # Mock JamfProClient (imported inside the function)
        mock_client_class = mocker.patch("jamfmcp.jamfsdk.JamfProClient")
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock(status_code=200)
        mock_client.pro_api_request.return_value = mock_response

        result = await validate_jamf_connection(
            "https://example.jamfcloud.com",
            "basic",
            {"username": "admin", "password": "secret"},
        )

        assert result is True
        mock_auth.assert_called_once_with(
            auth_type="basic",
            server="https://example.jamfcloud.com",
            username="admin",
            password="secret",
        )
        mock_client.pro_api_request.assert_called_once_with("get", "v1/auth")

    @pytest.mark.asyncio
    async def test_validate_jamf_connection_oauth_success(self, mocker: MockerFixture) -> None:
        """
        Test successful Jamf connection validation with OAuth.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock JamfAuth
        mock_auth = mocker.patch("jamfmcp.cli.JamfAuth")
        mock_auth_instance = MagicMock()
        mock_auth.return_value = mock_auth_instance
        mock_auth_instance.server = "https://example.jamfcloud.com"
        mock_auth_instance.get_credentials_provider.return_value = MagicMock()

        # Mock JamfProClient (imported inside the function)
        mock_client_class = mocker.patch("jamfmcp.jamfsdk.JamfProClient")
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock(status_code=200)
        mock_client.pro_api_request.return_value = mock_response

        result = await validate_jamf_connection(
            "https://example.jamfcloud.com",
            "oauth",
            {"client_id": "client123", "client_secret": "secret456"},
        )

        assert result is True
        mock_auth.assert_called_once_with(
            auth_type="oauth",
            server="https://example.jamfcloud.com",
            client_id="client123",
            client_secret="secret456",
        )

    @pytest.mark.asyncio
    async def test_validate_jamf_connection_failure(self, mocker: MockerFixture) -> None:
        """
        Test failed Jamf connection validation.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock JamfAuth to raise an exception
        mock_auth = mocker.patch("jamfmcp.cli.JamfAuth")
        mock_auth.side_effect = Exception("Connection failed")

        # Mock click.echo to capture output
        mock_echo = mocker.patch("jamfmcp.cli.click.echo")

        result = await validate_jamf_connection(
            "https://example.jamfcloud.com",
            "basic",
            {"username": "admin", "password": "wrong"},
        )

        assert result is False
        # Check that error message was printed
        assert any("Connection failed" in str(call) for call in mock_echo.call_args_list)


class TestCLICommands:
    """
    Tests for CLI commands.
    """

    @pytest.mark.asyncio
    async def test_cli_version(self) -> None:
        """
        Test CLI version option.
        """
        runner = CliRunner()
        result = await runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()

    @pytest.mark.asyncio
    async def test_cli_help(self) -> None:
        """
        Test CLI help option.
        """
        runner = CliRunner()
        result = await runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "JamfMCP CLI" in result.output
        assert "setup" in result.output
        assert "validate" in result.output

    @pytest.mark.asyncio
    async def test_setup_dry_run(self, mocker: MockerFixture) -> None:
        """
        Test setup command in dry-run mode.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "secret",
                "--dry-run",
            ],
        )

        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.output
        assert "fastmcp install claude-desktop jamfmcp.server:mcp" in result.output
        assert "JAMF_URL=https://example.jamfcloud.com" in result.output
        assert "***" in result.output  # Password should be masked

    @pytest.mark.asyncio
    async def test_setup_missing_fastmcp(self, mocker: MockerFixture) -> None:
        """
        Test setup command when FastMCP is not installed.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=False)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "secret",
            ],
        )

        assert result.exit_code == 0
        assert "FastMCP is not installed" in result.output
        assert "pip install fastmcp" in result.output

    @pytest.mark.asyncio
    async def test_setup_missing_uv(self, mocker: MockerFixture) -> None:
        """
        Test setup command when uv is not installed.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=True)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=False)

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "secret",
            ],
        )

        assert result.exit_code == 0
        assert "'uv' is not installed" in result.output
        assert "brew install uv" in result.output

    @pytest.mark.asyncio
    async def test_setup_basic_auth_success(self, mocker: MockerFixture) -> None:
        """
        Test successful setup with basic authentication.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=True)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock subprocess.run for fastmcp install
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "secret",
                "--server-name",
                "my-jamf",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully configured claude-desktop" in result.output
        assert "Restart Claude Desktop" in result.output

        # Verify the fastmcp install command was called correctly
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0:4] == ["fastmcp", "install", "claude-desktop", "jamfmcp.server:mcp"]
        assert "--name" in cmd
        assert "my-jamf" in cmd
        assert "--env" in cmd
        assert "JAMF_URL=https://example.jamfcloud.com" in cmd
        assert "--with" in cmd
        assert "jamfmcp" in cmd

    @pytest.mark.asyncio
    async def test_setup_oauth_success(self, mocker: MockerFixture) -> None:
        """
        Test successful setup with OAuth authentication.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=True)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock subprocess.run for fastmcp install
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "cursor",
                "--auth-type",
                "oauth",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--skip-validation",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully configured cursor" in result.output

        # Verify OAuth credentials were passed
        cmd = mock_run.call_args[0][0]
        assert "JAMF_AUTH_TYPE=oauth" in cmd
        assert "JAMF_CLIENT_ID=client123" in cmd
        assert "JAMF_CLIENT_SECRET=secret456" in cmd

    @pytest.mark.asyncio
    async def test_setup_cursor_with_workspace(self, mocker: MockerFixture) -> None:
        """
        Test setup for Cursor with workspace option.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=True)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock subprocess.run for fastmcp install
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # Create a temporary directory for workspace
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            runner = CliRunner()
            result = await runner.invoke(
                cli,
                [
                    "setup",
                    "--platform",
                    "cursor",
                    "--url",
                    "https://example.jamfcloud.com",
                    "--username",
                    "admin",
                    "--password",
                    "secret",
                    "--workspace",
                    tmpdir,
                    "--skip-validation",
                ],
            )

            assert result.exit_code == 0
            assert "Successfully configured cursor" in result.output
            assert f"Open Cursor in workspace: {tmpdir}" in result.output

            # Verify workspace was passed to fastmcp
            cmd = mock_run.call_args[0][0]
            assert "--workspace" in cmd
            assert tmpdir in cmd

    @pytest.mark.asyncio
    async def test_setup_mcp_json_output(self, mocker: MockerFixture) -> None:
        """
        Test setup for mcp-json platform.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=True)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock subprocess.run for fastmcp install
        mock_run = mocker.patch("subprocess.run")
        json_output = '{"jamfmcp": {"command": "uv", "args": ["run"]}}'
        mock_run.return_value = MagicMock(returncode=0, stdout=json_output, stderr="")

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "mcp-json",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "secret",
                "--skip-validation",
            ],
        )

        assert result.exit_code == 0
        assert "MCP JSON configuration generated" in result.output
        assert json_output in result.output

    @pytest.mark.asyncio
    async def test_validate_command_success(self, mocker: MockerFixture) -> None:
        """
        Test validate command with successful connection.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "validate",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "secret",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully connected to Jamf Pro!" in result.output
        assert "Server: https://example.jamfcloud.com" in result.output

    @pytest.mark.asyncio
    async def test_validate_command_failure(self, mocker: MockerFixture) -> None:
        """
        Test validate command with failed connection.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = False

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "validate",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "wrong",
            ],
        )

        assert result.exit_code == 1
        assert "Failed to connect to Jamf Pro" in result.output
        assert "Please check:" in result.output

    @pytest.mark.asyncio
    async def test_setup_prompts_for_missing_values(self, mocker: MockerFixture) -> None:
        """
        Test that setup prompts for missing values.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=True)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock subprocess.run for fastmcp install
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        runner = CliRunner()
        # Provide input for prompts
        result = await runner.invoke(
            cli,
            ["setup", "--platform", "claude-desktop"],
            input="https://example.jamfcloud.com\nadmin\nsecret\n",
        )

        assert result.exit_code == 0
        assert "Jamf Pro server URL:" in result.output
        assert "Username:" in result.output
        assert "Password:" in result.output

    @pytest.mark.asyncio
    async def test_setup_verbose_mode(self, mocker: MockerFixture) -> None:
        """
        Test setup command with verbose output.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_fastmcp_installed", return_value=True)
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock subprocess.run for fastmcp install
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--username",
                "admin",
                "--password",
                "secret",
                "--verbose",
            ],
        )

        assert result.exit_code == 0
        assert "Validating Jamf Pro connection..." in result.output
        assert "Running:" in result.output
        # Password should be masked even in verbose mode
        assert "***" in result.output
