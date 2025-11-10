"""
Unit tests for the JamfMCP CLI.
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, mock_open

import pytest
from asyncclick.testing import CliRunner
from pytest_mock import MockerFixture

from jamfmcp.cli import (
    SERVER_NAME,
    backup_existing_config,
    check_dependencies,
    cli,
    detect_installed_platforms,
    generate_env_vars,
    generate_mcp_config,
    get_platform_config_path,
    setup_claude_code,
    setup_gemini_cli,
    setup_with_fastmcp,
    validate_jamf_connection,
    write_platform_config,
)


class TestHelperFunctions:
    """Tests for CLI helper functions."""

    @pytest.mark.asyncio
    async def test_get_platform_config_path_claude_desktop_darwin(
        self, mocker: MockerFixture
    ) -> None:
        """Test getting Claude Desktop config path on macOS."""
        mocker.patch("platform.system", return_value="Darwin")
        path = await get_platform_config_path("claude-desktop")
        assert path is not None
        assert "Library/Application Support/Claude" in str(path)

    @pytest.mark.asyncio
    async def test_get_platform_config_path_claude_desktop_linux(
        self, mocker: MockerFixture
    ) -> None:
        """Test getting Claude Desktop config path on Linux."""
        mocker.patch("platform.system", return_value="Linux")
        path = await get_platform_config_path("claude-desktop")
        assert path is not None
        assert ".config/Claude" in str(path)

    @pytest.mark.asyncio
    async def test_get_platform_config_path_cursor(self) -> None:
        """Test getting Cursor config path."""
        path = await get_platform_config_path("cursor")
        assert path is not None
        assert ".cursor/mcp.json" in str(path)

    @pytest.mark.asyncio
    async def test_get_platform_config_path_cli_platforms(self) -> None:
        """Test getting config paths for CLI-based platforms."""
        assert await get_platform_config_path("claude-code") is None
        assert await get_platform_config_path("gemini-cli") is None
        assert await get_platform_config_path("mcp-json") is None

    @pytest.mark.asyncio
    async def test_generate_env_vars_basic_auth(self) -> None:
        """Test generating environment variables with basic authentication."""
        env_vars = await generate_env_vars(
            "basic",
            "https://test.jamfcloud.com",
            {"username": "testuser", "password": "testpass"},
        )

        assert env_vars["JAMF_URL"] == "https://test.jamfcloud.com"
        assert env_vars["JAMF_AUTH_TYPE"] == "basic"
        assert env_vars["JAMF_USERNAME"] == "testuser"
        assert env_vars["JAMF_PASSWORD"] == "testpass"

    @pytest.mark.asyncio
    async def test_generate_env_vars_oauth(self) -> None:
        """Test generating environment variables with OAuth authentication."""
        env_vars = await generate_env_vars(
            "oauth",
            "https://test.jamfcloud.com",
            {"client_id": "test-id", "client_secret": "test-secret"},
        )

        assert env_vars["JAMF_URL"] == "https://test.jamfcloud.com"
        assert env_vars["JAMF_AUTH_TYPE"] == "oauth"
        assert env_vars["JAMF_CLIENT_ID"] == "test-id"
        assert env_vars["JAMF_CLIENT_SECRET"] == "test-secret"

    @pytest.mark.asyncio
    async def test_generate_mcp_config_basic_auth(self) -> None:
        """Test generating MCP config with basic authentication."""
        config = await generate_mcp_config(
            "basic",
            "https://test.jamfcloud.com",
            {"username": "testuser", "password": "testpass"},
        )

        assert "mcpServers" in config
        assert SERVER_NAME in config["mcpServers"]
        server_config = config["mcpServers"][SERVER_NAME]

        assert server_config["command"] == "uvx"
        assert server_config["args"] == [
            "--from",
            "jamfmcp",
            "fastmcp",
            "run",
            "jamfmcp.server:mcp",
        ]
        assert server_config["env"]["JAMF_URL"] == "https://test.jamfcloud.com"
        assert server_config["env"]["JAMF_AUTH_TYPE"] == "basic"
        assert server_config["env"]["JAMF_USERNAME"] == "testuser"
        assert server_config["env"]["JAMF_PASSWORD"] == "testpass"

    @pytest.mark.asyncio
    async def test_generate_mcp_config_oauth(self) -> None:
        """Test generating MCP config with OAuth authentication."""
        config = await generate_mcp_config(
            "oauth",
            "https://test.jamfcloud.com",
            {"client_id": "test-id", "client_secret": "test-secret"},
        )

        server_config = config["mcpServers"][SERVER_NAME]
        assert server_config["env"]["JAMF_AUTH_TYPE"] == "oauth"
        assert server_config["env"]["JAMF_CLIENT_ID"] == "test-id"
        assert server_config["env"]["JAMF_CLIENT_SECRET"] == "test-secret"

    @pytest.mark.asyncio
    async def test_check_dependencies(self, mocker: MockerFixture) -> None:
        """Test checking for dependencies."""
        mock_run = mocker.patch("subprocess.run")

        # Mock successful command executions
        mock_run.return_value = MagicMock(returncode=0)

        deps = await check_dependencies()

        assert deps["uv"] is True
        assert deps["claude"] is True
        assert deps["gemini"] is True

    @pytest.mark.asyncio
    async def test_check_dependencies_missing(self, mocker: MockerFixture) -> None:
        """Test checking for dependencies when some are missing."""
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = FileNotFoundError()

        deps = await check_dependencies()

        assert deps["uv"] is False
        assert deps["claude"] is False
        assert deps["gemini"] is False

    @pytest.mark.asyncio
    async def test_backup_existing_config(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """Test backing up existing configuration."""
        # Create a test config file
        config_file = tmp_path / "config.json"
        config_file.write_text('{"test": "data"}')

        # Mock datetime for consistent backup naming
        mock_datetime = mocker.patch("jamfmcp.cli.datetime")
        mock_datetime.now.return_value.strftime.return_value = "20240101_120000"

        # Mock click.echo to suppress output
        mocker.patch("jamfmcp.cli.click.echo")

        await backup_existing_config(config_file)

        # Check backup was created
        backup_file = tmp_path / "config.backup.20240101_120000.json"
        assert backup_file.exists()
        assert backup_file.read_text() == '{"test": "data"}'

    @pytest.mark.asyncio
    async def test_detect_installed_platforms(self, mocker: MockerFixture) -> None:
        """Test detecting installed platforms."""
        # Mock config path existence
        mock_get_path = mocker.patch("jamfmcp.cli.get_platform_config_path")
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_get_path.return_value = mock_path

        # Mock dependency check
        mocker.patch(
            "jamfmcp.cli.check_dependencies",
            return_value={"uv": True, "claude": True, "gemini": False},
        )

        platforms = await detect_installed_platforms()

        assert "claude-desktop" in platforms
        assert "cursor" in platforms
        assert "claude-code" in platforms
        assert "gemini-cli" not in platforms

    @pytest.mark.asyncio
    async def test_validate_jamf_connection_success(self, mocker: MockerFixture) -> None:
        """Test successful Jamf connection validation."""
        # Mock JamfAuth
        mock_auth = mocker.patch("jamfmcp.cli.JamfAuth")

        # Mock JamfProClient - it's imported inside the function
        mock_client_class = mocker.patch("jamfmcp.jamfsdk.JamfProClient")
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.pro_api_request.return_value = MagicMock(status_code=200)
        mock_client_class.return_value = mock_client

        result = await validate_jamf_connection(
            "https://test.jamfcloud.com", "basic", {"username": "test", "password": "pass"}
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_validate_jamf_connection_failure(self, mocker: MockerFixture) -> None:
        """Test failed Jamf connection validation."""
        mocker.patch("jamfmcp.cli.JamfAuth")
        mocker.patch("jamfmcp.jamfsdk.JamfProClient", side_effect=Exception("Connection failed"))
        mocker.patch("jamfmcp.cli.click.echo")

        result = await validate_jamf_connection(
            "https://test.jamfcloud.com", "basic", {"username": "test", "password": "pass"}
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_setup_claude_code(self, mocker: MockerFixture) -> None:
        """Test setting up Claude Code configuration."""
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0)
        mocker.patch("jamfmcp.cli.click.echo")

        config = await generate_mcp_config(
            "basic", "https://test.jamfcloud.com", {"username": "test", "password": "pass"}
        )

        await setup_claude_code(config)

        # Verify subprocess was called with correct arguments
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "claude"
        assert args[1] == "mcp"
        assert args[2] == "add"
        assert args[3] == SERVER_NAME

    @pytest.mark.asyncio
    async def test_setup_gemini_cli(self, mocker: MockerFixture) -> None:
        """Test setting up Gemini CLI configuration."""
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value = MagicMock(returncode=0)
        mocker.patch("jamfmcp.cli.click.echo")

        config = await generate_mcp_config(
            "oauth", "https://test.jamfcloud.com", {"client_id": "id", "client_secret": "secret"}
        )

        await setup_gemini_cli(config)

        # Verify subprocess was called with correct arguments
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "gemini"
        assert args[1] == "mcp"
        assert args[2] == "add"
        assert args[3] == SERVER_NAME

    @pytest.mark.asyncio
    async def test_write_platform_config_new_file(
        self, mocker: MockerFixture, tmp_path: Path
    ) -> None:
        """Test writing platform config to a new file."""
        config_path = tmp_path / "config.json"
        mocker.patch("jamfmcp.cli.get_platform_config_path", return_value=config_path)
        mocker.patch("jamfmcp.cli.click.echo")

        config = await generate_mcp_config(
            "basic", "https://test.jamfcloud.com", {"username": "test", "password": "pass"}
        )

        await write_platform_config("cursor", config)

        assert config_path.exists()
        written_config = json.loads(config_path.read_text())
        assert "mcpServers" in written_config
        assert SERVER_NAME in written_config["mcpServers"]

    @pytest.mark.asyncio
    async def test_write_platform_config_existing_file(
        self, mocker: MockerFixture, tmp_path: Path
    ) -> None:
        """Test writing platform config to an existing file."""
        config_path = tmp_path / "config.json"
        existing_config = {"mcpServers": {"other-server": {"command": "test"}}}
        config_path.write_text(json.dumps(existing_config))

        mocker.patch("jamfmcp.cli.get_platform_config_path", return_value=config_path)
        mocker.patch("jamfmcp.cli.backup_existing_config")
        mocker.patch("jamfmcp.cli.click.echo")

        config = await generate_mcp_config(
            "basic", "https://test.jamfcloud.com", {"username": "test", "password": "pass"}
        )

        await write_platform_config("cursor", config)

        written_config = json.loads(config_path.read_text())
        assert "other-server" in written_config["mcpServers"]
        assert SERVER_NAME in written_config["mcpServers"]

    @pytest.mark.asyncio
    async def test_setup_with_fastmcp(self, mocker: MockerFixture) -> None:
        """Test setup using FastMCP CLI."""
        # Mock subprocess.run
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""

        env_vars = {
            "JAMF_URL": "https://test.jamfcloud.com",
            "JAMF_AUTH_TYPE": "basic",
            "JAMF_USERNAME": "testuser",
            "JAMF_PASSWORD": "testpass",
        }

        result = await setup_with_fastmcp("claude-desktop", env_vars, verbose=True)
        assert result is True

        # Check the command that was called
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "fastmcp"
        assert cmd[1] == "install"
        assert cmd[2] == "claude-desktop"
        assert cmd[3] == "jamfmcp.server:mcp"
        assert "--env" in cmd
        assert "JAMF_URL=https://test.jamfcloud.com" in cmd
        assert "--with" in cmd
        assert "jamfmcp" in cmd

    @pytest.mark.asyncio
    async def test_setup_with_fastmcp_with_workspace(self, mocker: MockerFixture) -> None:
        """Test setup using FastMCP CLI with workspace option."""
        # Mock subprocess.run
        mock_run = mocker.patch("subprocess.run")
        mock_run.return_value.returncode = 0

        env_vars = {"JAMF_URL": "https://test.jamfcloud.com"}

        result = await setup_with_fastmcp("cursor", env_vars, workspace="/test/workspace")
        assert result is True

        # Check that workspace option was included
        cmd = mock_run.call_args[0][0]
        assert "--workspace" in cmd
        assert "/test/workspace" in cmd


class TestCLICommands:
    """
    Tests for CLI commands.
    """

    @pytest.mark.asyncio
    async def test_cli_version(self) -> None:
        """Test CLI version option."""
        runner = CliRunner()
        result = await runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()

    @pytest.mark.asyncio
    async def test_cli_help(self) -> None:
        """Test CLI help output."""
        runner = CliRunner()
        result = await runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "JamfMCP CLI" in result.output
        assert "setup" in result.output
        assert "validate" in result.output
        assert "doctor" in result.output
        assert "update" in result.output

    @pytest.mark.asyncio
    async def test_setup_command_dry_run(self, mocker: MockerFixture) -> None:
        """Test setup command with dry-run flag."""
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})
        mocker.patch("jamfmcp.cli.validate_jamf_connection", return_value=True)

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "mcp-json",
                "--auth-type",
                "basic",
                "--url",
                "https://test.jamfcloud.com",
                "--username",
                "testuser",
                "--password",
                "testpass",
                "--dry-run",
            ],
        )

        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.output
        # The dry-run mode now shows the fastmcp command that would be run
        assert "fastmcp install mcp-json" in result.output
        assert "jamfmcp.server:mcp" in result.output
        assert "--env JAMF_URL=https://test.jamfcloud.com" in result.output

    @pytest.mark.asyncio
    async def test_setup_command_interactive(self, mocker: MockerFixture) -> None:
        """Test setup command with interactive prompts."""
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})
        mocker.patch("jamfmcp.cli.validate_jamf_connection", return_value=True)
        mocker.patch("jamfmcp.cli.write_platform_config")

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            ["setup", "--platform", "cursor", "--auth-type", "basic"],
            input="https://test.jamfcloud.com\ntestuser\ntestpass\n",
        )

        assert result.exit_code == 0
        assert "Setting up JamfMCP" in result.output

    @pytest.mark.asyncio
    async def test_setup_command_oauth(self, mocker: MockerFixture) -> None:
        """Test setup command with OAuth authentication."""
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})
        mocker.patch("jamfmcp.cli.validate_jamf_connection", return_value=True)
        mocker.patch("jamfmcp.cli.write_platform_config")

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
                "https://test.jamfcloud.com",
                "--client-id",
                "test-id",
                "--client-secret",
                "test-secret",
            ],
        )

        assert result.exit_code == 0

    @pytest.mark.asyncio
    async def test_setup_command_missing_uv(self, mocker: MockerFixture) -> None:
        """Test setup command when uv is not installed."""
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": False})

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "cursor",
                "--url",
                "https://test.jamfcloud.com",
                "--username",
                "test",
                "--password",
                "pass",
            ],
        )

        assert result.exit_code == 0
        assert "'uv' is not installed" in result.output

    @pytest.mark.asyncio
    async def test_validate_command_all_platforms(self, mocker: MockerFixture) -> None:
        """Test validate command for all platforms."""
        mocker.patch("jamfmcp.cli.detect_installed_platforms", return_value=["cursor"])
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})

        config_path = MagicMock()
        config_path.exists.return_value = True
        mocker.patch("jamfmcp.cli.get_platform_config_path", return_value=config_path)

        mock_open_file = mocker.patch(
            "builtins.open",
            mock_open(
                read_data=json.dumps(
                    {
                        "mcpServers": {
                            SERVER_NAME: {
                                "env": {
                                    "JAMF_URL": "https://test.jamfcloud.com",
                                    "JAMF_AUTH_TYPE": "basic",
                                    "JAMF_USERNAME": "test",
                                    "JAMF_PASSWORD": "pass",
                                }
                            }
                        }
                    }
                )
            ),
        )

        mocker.patch("jamfmcp.cli.validate_jamf_connection", return_value=True)

        runner = CliRunner()
        result = await runner.invoke(cli, ["validate", "--platform", "all"])

        assert result.exit_code == 0
        assert "Validating JamfMCP configuration" in result.output

    @pytest.mark.asyncio
    async def test_validate_command_specific_platform(self, mocker: MockerFixture) -> None:
        """Test validate command for specific platform."""
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True, "claude": True})

        runner = CliRunner()
        result = await runner.invoke(cli, ["validate", "--platform", "claude-code"])

        assert result.exit_code == 0
        assert "claude-code" in result.output

    @pytest.mark.asyncio
    async def test_doctor_command(self, mocker: MockerFixture) -> None:
        """Test doctor command."""
        mocker.patch(
            "jamfmcp.cli.check_dependencies",
            return_value={"uv": True, "claude": False, "gemini": False},
        )
        mocker.patch("jamfmcp.cli.detect_installed_platforms", return_value=[])

        runner = CliRunner()
        result = await runner.invoke(cli, ["doctor"])

        assert result.exit_code == 0
        assert "JamfMCP Doctor" in result.output
        assert "System Information" in result.output
        assert "Dependencies" in result.output

    @pytest.mark.asyncio
    async def test_doctor_command_verbose(self, mocker: MockerFixture) -> None:
        """Test doctor command with verbose flag."""
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})
        mocker.patch("jamfmcp.cli.detect_installed_platforms", return_value=["cursor"])

        config_path = MagicMock()
        config_path.exists.return_value = True
        mocker.patch("jamfmcp.cli.get_platform_config_path", return_value=config_path)

        mocker.patch(
            "builtins.open",
            mock_open(
                read_data=json.dumps(
                    {
                        "mcpServers": {
                            SERVER_NAME: {
                                "env": {
                                    "JAMF_URL": "https://test.jamfcloud.com",
                                    "JAMF_AUTH_TYPE": "basic",
                                    "JAMF_USERNAME": "test",
                                    "JAMF_PASSWORD": "pass",
                                }
                            }
                        }
                    }
                )
            ),
        )

        mocker.patch("jamfmcp.cli.validate_jamf_connection", return_value=True)

        runner = CliRunner()
        result = await runner.invoke(cli, ["doctor", "--verbose"])

        assert result.exit_code == 0

    @pytest.mark.asyncio
    async def test_update_command_check_only(self, mocker: MockerFixture) -> None:
        """Test update command with check-only flag."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "1.0.1"}}
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mocker.patch("httpx.AsyncClient", return_value=mock_client)
        mocker.patch("jamfmcp.cli.__version__", "1.0.0")

        runner = CliRunner()
        result = await runner.invoke(cli, ["update", "--check-only"])

        assert result.exit_code == 0
        assert "Update available" in result.output

    @pytest.mark.asyncio
    async def test_update_command_install(self, mocker: MockerFixture) -> None:
        """Test update command installing updates."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "1.0.1"}}
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mocker.patch("httpx.AsyncClient", return_value=mock_client)
        mocker.patch("jamfmcp.cli.__version__", "1.0.0")
        mocker.patch("subprocess.run", return_value=MagicMock(returncode=0))
        mocker.patch("jamfmcp.cli.detect_installed_platforms", return_value=[])

        runner = CliRunner()
        result = await runner.invoke(cli, ["update"], input="y\n")

        assert result.exit_code == 0

    @pytest.mark.asyncio
    async def test_update_command_config_migration(
        self, mocker: MockerFixture, tmp_path: Path
    ) -> None:
        """Test update command migrating old configurations."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "1.0.0"}}
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mocker.patch("httpx.AsyncClient", return_value=mock_client)
        mocker.patch("jamfmcp.cli.__version__", "1.0.0")

        # Create old format config
        config_path = tmp_path / "config.json"
        old_config = {
            "mcpServers": {
                SERVER_NAME: {
                    "command": "python",
                    "args": ["-m", "jamfmcp.server"],
                    "env": {"JAMF_URL": "https://test.jamfcloud.com"},
                }
            }
        }
        config_path.write_text(json.dumps(old_config))

        mocker.patch("jamfmcp.cli.detect_installed_platforms", return_value=["cursor"])
        mocker.patch("jamfmcp.cli.get_platform_config_path", return_value=config_path)
        mocker.patch("jamfmcp.cli.backup_existing_config")

        runner = CliRunner()
        result = await runner.invoke(cli, ["update"])

        assert result.exit_code == 0

        # Check config was updated
        updated_config = json.loads(config_path.read_text())
        assert updated_config["mcpServers"][SERVER_NAME]["command"] == "uv"


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_invalid_platform_config_json(
        self, mocker: MockerFixture, tmp_path: Path
    ) -> None:
        """Test handling of invalid JSON in platform config."""
        config_path = tmp_path / "config.json"
        config_path.write_text("invalid json{")

        mocker.patch("jamfmcp.cli.get_platform_config_path", return_value=config_path)
        mocker.patch("jamfmcp.cli.click.echo")

        config = await generate_mcp_config(
            "basic", "https://test.jamfcloud.com", {"username": "test", "password": "pass"}
        )

        await write_platform_config("cursor", config)

        # Should create new valid config despite invalid existing one
        assert config_path.exists()
        new_config = json.loads(config_path.read_text())
        assert "mcpServers" in new_config

    @pytest.mark.asyncio
    async def test_url_normalization(self, mocker: MockerFixture) -> None:
        """Test URL normalization in setup command."""
        # Mock check_dependencies to avoid subprocess calls
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            ["setup", "--platform", "mcp-json", "--auth-type", "basic", "--dry-run"],
            input="test.jamfcloud.com\ntestuser\ntestpass\n",
        )

        assert "https://test.jamfcloud.com" in result.output

    @pytest.mark.asyncio
    async def test_connection_failure_continue(self, mocker: MockerFixture) -> None:
        """Test continuing setup after connection failure."""
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})
        mocker.patch("jamfmcp.cli.validate_jamf_connection", return_value=False)
        mocker.patch("jamfmcp.cli.write_platform_config")

        runner = CliRunner()
        result = await runner.invoke(
            cli,
            [
                "setup",
                "--platform",
                "cursor",
                "--url",
                "https://test.jamfcloud.com",
                "--username",
                "test",
                "--password",
                "pass",
            ],
            input="y\n",  # Continue anyway
        )

        assert result.exit_code == 0

    @pytest.mark.asyncio
    async def test_platform_not_supported_on_os(self, mocker: MockerFixture) -> None:
        """Test platform not supported on current OS."""
        mocker.patch("platform.system", return_value="Windows")
        path = await get_platform_config_path("claude-desktop")
        assert path is None

    @pytest.mark.asyncio
    async def test_empty_environment_variables(
        self, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test doctor command with no environment variables set."""
        # Mock check_dependencies to avoid subprocess calls
        mocker.patch("jamfmcp.cli.check_dependencies", return_value={"uv": True})
        # Mock detect_installed_platforms to avoid file system checks
        mocker.patch("jamfmcp.cli.detect_installed_platforms", return_value=[])

        for var in ["JAMF_URL", "JAMF_AUTH_TYPE", "JAMF_USERNAME", "JAMF_CLIENT_ID"]:
            monkeypatch.delenv(var, raising=False)  # Clear all Jamf env vars

        runner = CliRunner()
        result = await runner.invoke(cli, ["doctor"])

        assert result.exit_code == 0
        assert "No Jamf environment variables found" in result.output
