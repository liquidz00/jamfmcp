"""
Unit tests for the JamfMCP CLI.
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from asyncclick.testing import CliRunner
from pytest_mock import MockerFixture

from jamfmcp.cli import (
    build_config,
    check_uv_installed,
    format_err,
    get_config_path,
    get_project_paths,
    main,
    save_mcp_config,
    show_next_steps,
    validate_jamf_connection,
)


class TestHelperFunctions:
    """
    Tests for CLI helper functions.
    """

    def test_format_err(self, mocker: MockerFixture) -> None:
        """
        Test error formatting function.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_echo = mocker.patch("jamfmcp.cli.click.echo")
        mock_style = mocker.patch("jamfmcp.cli.click.style")
        mock_style.return_value = "styled_error"

        test_exception = Exception("Test error message")
        format_err(test_exception)

        mock_style.assert_called_once_with("❌ Error: Test error message", fg="red", bold=True)
        mock_echo.assert_called_once_with("styled_error", err=True)

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

    def test_check_uv_installed_failure(self, mocker: MockerFixture) -> None:
        """
        Test checking if uv is installed when command fails.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=1)

        result = check_uv_installed()

        assert result is False

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
            {"JAMF_CLIENT_ID": "client123", "JAMF_CLIENT_SECRET": "secret456"},
        )

        assert result is True
        mock_auth.assert_called_once_with(
            server="https://example.jamfcloud.com",
            client_id="client123",
            client_secret="secret456",
        )
        mock_client.pro_api_request.assert_called_once_with("get", "v1/auth")

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
            {"JAMF_CLIENT_ID": "admin", "JAMF_CLIENT_SECRET": "wrong"},
        )

        assert result is False
        # Check that error message was printed
        assert any("Connection failed" in str(call) for call in mock_echo.call_args_list)

    def test_get_project_paths(self, mocker: MockerFixture) -> None:
        """
        Test getting project paths.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock jamfmcp module path
        mock_jamfmcp = MagicMock()
        mock_jamfmcp.__file__ = "/path/to/project/src/jamfmcp/__init__.py"
        mocker.patch.dict("sys.modules", {"jamfmcp": mock_jamfmcp})

        result = get_project_paths()

        assert str(result) == "/path/to/project/src"

    def test_get_config_path_claude_desktop(self) -> None:
        """
        Test getting config path for Claude Desktop.
        """
        result = get_config_path("claude-desktop")
        expected = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
        assert result == expected

    def test_get_config_path_claude_code(self) -> None:
        """
        Test getting config path for Claude Code.
        """
        result = get_config_path("claude-code")
        expected = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
        assert result == expected

    def test_get_config_path_cursor_global(self) -> None:
        """
        Test getting global config path for Cursor.
        """
        result = get_config_path("cursor")
        expected = Path.home() / ".cursor/mcp.json"
        assert result == expected

    def test_get_config_path_cursor_workspace(self) -> None:
        """
        Test getting workspace config path for Cursor.
        """
        workspace = Path("/test/workspace")
        result = get_config_path("cursor", workspace)
        expected = workspace / ".mcp.json"
        assert result == expected

    def test_get_config_path_gemini_global(self) -> None:
        """
        Test getting global config path for Gemini CLI.
        """
        result = get_config_path("gemini-cli")
        expected = Path.home() / ".gemini/settings.json"
        assert result == expected

    def test_get_config_path_gemini_workspace(self) -> None:
        """
        Test getting workspace config path for Gemini CLI.
        """
        workspace = Path("/test/workspace")
        result = get_config_path("gemini-cli", workspace)
        expected = workspace / ".gemini/settings.json"
        assert result == expected

    def test_build_config_dev_mode(self, mocker: MockerFixture) -> None:
        """
        Test building config in development mode.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mocker.patch("jamfmcp.cli.get_project_paths", return_value=Path("/project/root"))

        credentials = {
            "JAMF_URL": "https://example.jamfcloud.com",
            "JAMF_CLIENT_ID": "client123",
            "JAMF_CLIENT_SECRET": "secret456",
        }

        result = build_config(dev=True, credentials=credentials)

        assert result == {
            "jamfmcp": {
                "command": "uv",
                "args": ["run", "--project", "/project/root", "jamfmcp"],
                "env": credentials,
            }
        }

    def test_build_config_pypi_mode(self) -> None:
        """
        Test building config in PyPI mode.
        """
        credentials = {
            "JAMF_URL": "https://example.jamfcloud.com",
            "JAMF_CLIENT_ID": "client123",
            "JAMF_CLIENT_SECRET": "secret456",
        }

        result = build_config(dev=False, credentials=credentials)

        assert result == {
            "jamfmcp": {
                "command": "uvx",
                "args": ["jamfmcp"],
                "env": credentials,
            }
        }

    def test_save_mcp_config_new_file(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """
        Test saving MCP config to a new file.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        :param tmp_path: Temporary directory path
        :type tmp_path: Path
        """
        config_path = tmp_path / "config.json"
        mocker.patch("jamfmcp.cli.get_config_path", return_value=config_path)

        config = {
            "jamfmcp": {
                "command": "uvx",
                "args": ["jamfmcp"],
                "env": {"JAMF_URL": "https://example.jamfcloud.com"},
            }
        }

        result = save_mcp_config(config, "claude-desktop", None)

        assert result is True
        assert config_path.exists()

        with open(config_path) as f:
            saved_data = json.load(f)

        assert saved_data == {"mcpServers": config}

    def test_save_mcp_config_existing_file(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """
        Test saving MCP config to an existing file (merge).

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        :param tmp_path: Temporary directory path
        :type tmp_path: Path
        """
        config_path = tmp_path / "config.json"
        mocker.patch("jamfmcp.cli.get_config_path", return_value=config_path)

        # Create existing config
        existing_data = {
            "mcpServers": {
                "other-server": {
                    "command": "other",
                    "args": [],
                }
            }
        }
        with open(config_path, "w") as f:
            json.dump(existing_data, f)

        # New config to merge
        config = {
            "jamfmcp": {
                "command": "uvx",
                "args": ["jamfmcp"],
                "env": {"JAMF_URL": "https://example.jamfcloud.com"},
            }
        }

        result = save_mcp_config(config, "claude-desktop", None)

        assert result is True

        with open(config_path) as f:
            saved_data = json.load(f)

        # Should have both servers
        assert "other-server" in saved_data["mcpServers"]
        assert "jamfmcp" in saved_data["mcpServers"]
        assert saved_data["mcpServers"]["jamfmcp"] == config["jamfmcp"]

    def test_show_next_steps_claude_desktop(self, mocker: MockerFixture) -> None:
        """
        Test showing next steps for Claude Desktop.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_echo = mocker.patch("jamfmcp.cli.click.echo")

        show_next_steps("claude-desktop", None)

        calls = [str(call) for call in mock_echo.call_args_list]
        assert any("Next steps:" in str(call) for call in calls)
        assert any("Restart Claude Desktop" in str(call) for call in calls)
        assert any("hammer icon" in str(call) for call in calls)

    def test_show_next_steps_cursor_global(self, mocker: MockerFixture) -> None:
        """
        Test showing next steps for Cursor (global).

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_echo = mocker.patch("jamfmcp.cli.click.echo")

        show_next_steps("cursor", None)

        calls = [str(call) for call in mock_echo.call_args_list]
        assert any("Click 'Install'" in str(call) for call in calls)
        assert any("Restart Cursor" in str(call) for call in calls)

    def test_show_next_steps_cursor_workspace(self, mocker: MockerFixture) -> None:
        """
        Test showing next steps for Cursor (workspace).

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mock_echo = mocker.patch("jamfmcp.cli.click.echo")
        workspace = Path("/test/workspace")

        show_next_steps("cursor", workspace)

        calls = [str(call) for call in mock_echo.call_args_list]
        assert any("Open Cursor in workspace" in str(call) for call in calls)
        assert any(str(workspace) in str(call) for call in calls)


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
        result = await runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()

    @pytest.mark.asyncio
    async def test_cli_help(self) -> None:
        """
        Test CLI help option.
        """
        runner = CliRunner()
        result = await runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Configure JamfMCP" in result.output
        assert "--platform" in result.output
        assert "--dev" in result.output

    @pytest.mark.asyncio
    async def test_setup_dry_run(self, mocker: MockerFixture) -> None:
        """
        Test setup command in dry-run mode.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--dry-run",
            ],
        )

        assert result.exit_code == 0
        assert "JamfMCP Configuration:" in result.output
        assert '"command": "uvx"' in result.output
        assert "jamfmcp" in result.output  # Check for jamfmcp in args
        assert "JAMF_URL" in result.output
        assert "JAMF_CLIENT_ID" in result.output

    @pytest.mark.asyncio
    async def test_setup_missing_uv(self, mocker: MockerFixture) -> None:
        """
        Test setup command when uv is not installed.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=False)

        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
            ],
        )

        assert result.exit_code == 0
        assert "'uv' is not installed" in result.output
        assert "brew install uv" in result.output

    @pytest.mark.asyncio
    async def test_setup_success_with_write(self, mocker: MockerFixture) -> None:
        """
        Test successful setup with write flag.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock save_mcp_config
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.return_value = True

        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--write",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully configured claude-desktop" in result.output
        assert "Restart Claude Desktop" in result.output

        # Verify save_mcp_config was called
        mock_save.assert_called_once()
        config = mock_save.call_args[0][0]
        assert "jamfmcp" in config
        assert config["jamfmcp"]["command"] == "uvx"

    @pytest.mark.asyncio
    async def test_setup_with_workspace(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """
        Test setup for Cursor with workspace option.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        :param tmp_path: Temporary directory path
        :type tmp_path: Path
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock save_mcp_config
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.return_value = True

        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "cursor",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--workspace",
                str(tmp_path),
                "--skip-validation",
                "--write",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully configured cursor" in result.output
        assert f"Open Cursor in workspace: {tmp_path}" in result.output

        # Verify workspace was passed to save_mcp_config
        mock_save.assert_called_once()
        assert mock_save.call_args[0][2] == tmp_path

    @pytest.mark.asyncio
    async def test_setup_dev_mode(self, mocker: MockerFixture) -> None:
        """
        Test setup in development mode.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)
        mocker.patch("jamfmcp.cli.get_project_paths", return_value=Path("/project/root"))

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock save_mcp_config
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.return_value = True

        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--dev",
                "--write",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully configured claude-desktop" in result.output

        # Verify dev mode config
        mock_save.assert_called_once()
        config = mock_save.call_args[0][0]
        assert config["jamfmcp"]["command"] == "uv"
        assert config["jamfmcp"]["args"] == ["run", "--project", "/project/root", "jamfmcp"]

    @pytest.mark.asyncio
    async def test_setup_prompts_for_missing_values(self, mocker: MockerFixture) -> None:
        """
        Test that setup prompts for missing values.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock save_mcp_config
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.return_value = True

        runner = CliRunner()
        # Provide input for prompts
        result = await runner.invoke(
            main,
            ["--platform", "claude-desktop", "--write"],
            input="https://example.jamfcloud.com\nclient123\nsecret456\n",
        )

        assert result.exit_code == 0
        assert "Jamf Pro server URL:" in result.output
        assert "Client ID:" in result.output
        assert "Client Secret:" in result.output

    @pytest.mark.asyncio
    async def test_setup_verbose_mode(self, mocker: MockerFixture) -> None:
        """
        Test setup command with verbose output.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock save_mcp_config
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.return_value = True

        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--verbose",
                "--write",
            ],
        )

        assert result.exit_code == 0
        assert "Validating Jamf Pro connection..." in result.output

    @pytest.mark.asyncio
    async def test_setup_validation_failure_continue(self, mocker: MockerFixture) -> None:
        """
        Test setup when validation fails but user continues.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation to fail
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = False

        # Mock save_mcp_config
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.return_value = True

        runner = CliRunner()
        # Provide 'y' to continue anyway
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "wrong",
                "--write",
            ],
            input="y\n",
        )

        assert result.exit_code == 0
        assert "Failed to connect to Jamf Pro" in result.output
        assert "Continue anyway?" in result.output
        assert "Successfully configured claude-desktop" in result.output

    @pytest.mark.asyncio
    async def test_setup_validation_failure_abort(self, mocker: MockerFixture) -> None:
        """
        Test setup when validation fails and user aborts.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation to fail
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = False

        runner = CliRunner()
        # Provide 'n' to abort
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "wrong",
                "--write",
            ],
            input="n\n",
        )

        assert result.exit_code == 0
        assert "Failed to connect to Jamf Pro" in result.output
        assert "Continue anyway?" in result.output
        assert "Successfully configured" not in result.output

    @pytest.mark.asyncio
    async def test_setup_url_protocol_handling(self, mocker: MockerFixture) -> None:
        """
        Test that URL protocol is added if missing.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mock_validate = mocker.patch("jamfmcp.cli.validate_jamf_connection")
        mock_validate.return_value = True

        # Mock save_mcp_config
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.return_value = True

        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "example.jamfcloud.com",  # No protocol
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--write",
            ],
        )

        assert result.exit_code == 0

        # Verify the URL was corrected
        mock_validate.assert_called_once()
        assert mock_validate.call_args[0][0] == "https://example.jamfcloud.com"

    @pytest.mark.asyncio
    async def test_setup_exception_handling(self, mocker: MockerFixture) -> None:
        """
        Test exception handling during setup.

        :param mocker: Pytest mocker fixture
        :type mocker: MockerFixture
        """
        # Mock dependencies check
        mocker.patch("jamfmcp.cli.check_uv_installed", return_value=True)

        # Mock validation
        mocker.patch("jamfmcp.cli.validate_jamf_connection", return_value=True)

        # Mock save_mcp_config to raise exception
        mock_save = mocker.patch("jamfmcp.cli.save_mcp_config")
        mock_save.side_effect = Exception("Failed to save config")

        runner = CliRunner()
        result = await runner.invoke(
            main,
            [
                "--platform",
                "claude-desktop",
                "--url",
                "https://example.jamfcloud.com",
                "--client-id",
                "client123",
                "--client-secret",
                "secret456",
                "--write",
            ],
        )

        assert result.exit_code == 0
        assert "Error: Failed to save config" in result.output
