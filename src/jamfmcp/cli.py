"""
JamfMCP CLI - Configuration tool for setting up JamfMCP with AI platforms.

This CLI helps users configure JamfMCP to work with various AI platforms like
Claude Desktop, Cursor, and others. It handles two installation modes:

1. PyPI Mode (default): For users who installed JamfMCP from PyPI
2. Development Mode (--dev): For developers working on JamfMCP source code

Both modes configure the MCP server to run locally on the user's machine.
The difference is how the server is invoked (uvx vs uv run).
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import asyncclick as click

from jamfmcp.__about__ import __version__
from jamfmcp.auth import JamfAuth

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def format_err(exc: Exception) -> None:
    """
    Format and display an error message to stderr.

    :param exc: The exception to format and display
    :type exc: Exception
    """
    click.echo(click.style(f"❌ Error: {str(exc)}", fg="red", bold=True), err=True)


async def validate_jamf_connection(url: str, credentials: dict[str, str]) -> bool:
    """
    Validate connection to Jamf Pro server.

    :param url: Jamf Pro server URL
    :type url: str
    :param credentials: Authentication credentials
    :type credentials: dict[str, str]
    :return: True if connection is valid
    :rtype: bool
    """
    try:
        auth = JamfAuth(
            server=url,
            client_id=credentials["JAMF_CLIENT_ID"],
            client_secret=credentials["JAMF_CLIENT_SECRET"],
        )

        # Test connection
        from jamfmcp.jamfsdk import JamfProClient

        async with JamfProClient(
            server=auth.server, credentials=auth.get_credentials_provider()
        ) as client:
            # Simple API call to verify connection
            # Note: pro_api_request already prepends /api/ to the resource path
            response = await client.pro_api_request("get", "v1/auth")
            return response.status_code == 200
    except Exception as e:
        click.echo(click.style(f"Connection failed: {str(e)}", fg="red"))
        return False


def check_uv_installed() -> bool:
    """
    Check if uv is installed.

    :return: True if uv is installed
    :rtype: bool
    """
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def show_next_steps(platform: str, workspace: Path | None) -> None:
    """
    Display next steps after successful configuration.

    :param platform: The AI platform that was configured
    :type platform: str
    :param workspace: Whether a workspace was specified (for Cursor, Gemini)
    :type workspace: Path | None
    :return: None
    :rtype: None
    """
    # Do not need to validate platform is proper type as this function
    # is only called after click validation
    match platform:
        case "claude-desktop":
            click.echo("\n📝 Next steps:")
            click.echo("1. Restart Claude Desktop completely")
            click.echo("2. Look for the hammer icon (🔨) in the input box")
            click.echo("3. Your JamfMCP tools are now available!")
        case "cursor":
            if workspace:
                click.echo("\n📝 Next steps:")
                click.echo(f"1. Open Cursor in workspace: {workspace}")
                click.echo("2. JamfMCP tools should now be available")
            else:
                click.echo("\n📝 Next steps:")
                click.echo("1. Click 'Install' in the Cursor prompt")
                click.echo("2. Restart Cursor or reload the window")
                click.echo("3. JamfMCP tools should now be available")
        case "claude-code":
            click.echo("\n📝 Configuration complete!")
            click.echo("JamfMCP has been added to Claude Code")
        case "gemini-cli":
            if workspace:
                click.echo("\n📝 Next steps:")
                click.echo(f"1. Use gemini in your workspace: {workspace}")
                click.echo("2. JamfMCP tools should now be available")
            else:
                click.echo("\n📝 Configuration complete!")
                click.echo("JamfMCP has been added to Gemini CLI")


def get_project_paths() -> Path:
    """
    Get the project root path for development mode.

    :return: Path to the project root directory
    :rtype: Path
    """
    import jamfmcp

    module_path = os.path.dirname(jamfmcp.__file__)
    project_root = os.path.dirname(module_path)

    return project_root


def get_config_path(platform: str, workspace: Path | None = None) -> Path:
    """
    Get the configuration file path for the specified platform.

    :param platform: The AI platform (claude-desktop, cursor, claude-code, gemini-cli)
    :type platform: str
    :param workspace: Optional workspace directory for project-specific configurations
    :type workspace: Path | None
    :return: Path to the platform's configuration file
    :rtype: Path
    """
    if platform == "claude-code" or platform == "claude-desktop":
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif platform == "cursor":
        if workspace:
            return workspace / ".mcp.json"
        else:
            return Path.home() / ".cursor/mcp.json"
    elif platform == "gemini-cli":
        if workspace:
            return workspace / ".gemini/settings.json"
        else:
            return Path.home() / ".gemini/settings.json"


def build_config(dev: bool, credentials: dict) -> dict[str, Any]:
    """
    Build the MCP server configuration.

    :param dev: Whether to configure for development mode
    :type dev: bool
    :param credentials: Jamf Pro credentials dictionary
    :type credentials: dict
    :return: MCP server configuration dictionary
    :rtype: dict[str, Any]
    """
    config = {"command": "", "args": [], "env": credentials}

    if dev:
        config["command"] = "uv"
        config["args"] = ["run", "--project", str(get_project_paths()), "jamfmcp"]
    else:
        config["command"] = "uvx"
        config["args"] = ["jamfmcp"]

    return {"jamfmcp": config}


def save_mcp_config(config: dict[str, Any], platform: str, workspace: Path | None) -> bool:
    """
    Save MCP configuration, merging with existing config if present.

    :param config: The MCP server configuration to save
    :type config: dict[str, Any]
    :param platform: The platform being configured
    :type platform: str
    :param workspace: Optional workspace path for cursor or Gemini
    :type workspace: Path | None
    :return: True if successful
    :rtype: bool
    """
    config_path = get_config_path(platform, workspace)

    # Read if exists already
    if config_path.exists():
        with open(config_path, "r") as file:
            data = json.load(file)

        if "mcpServers" not in data:
            data["mcpServers"] = {}

        # Merge in jamfmcp config
        data["mcpServers"].update(config)
    else:
        data = {"mcpServers": config}
        config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as file:
        json.dump(data, file, indent=2)

    return True


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option(
    "--platform",
    "-p",
    type=click.Choice(
        ["claude-desktop", "cursor", "claude-code", "gemini-cli"],
        case_sensitive=False,
    ),
    required=True,
    help="AI platform to configure",
)
@click.option(
    "--dev",
    "-d",
    is_flag=True,
    help="Configure for development mode (local source) instead of PyPI package",
)
@click.option(
    "--url",
    "-u",
    type=str,
    help="Jamf Pro server URL",
)
@click.option(
    "--client-id",
    type=str,
    help="Client ID for OAuth",
)
@click.option(
    "--client-secret",
    type=str,
    help="Client secret for OAuth",
)
@click.option(
    "--workspace",
    "-w",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Workspace directory for Cursor project-specific installation",
)
@click.option(
    "--skip-validation",
    is_flag=True,
    help="Skip Jamf Pro connection validation",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making changes",
)
@click.option(
    "--write",
    is_flag=True,
    help="Write directly to configuration file",
)
async def main(
    platform: str,
    dev: bool,
    url: str | None,
    client_id: str | None,
    client_secret: str | None,
    workspace: Path | None,
    skip_validation: bool,
    verbose: bool,
    dry_run: bool,
    write: bool,
) -> None:
    """
    Configure JamfMCP for your AI platform.

    \f
    This command collects your Jamf Pro credentials and configures JamfMCP
    to run locally on your machine with your chosen AI platform.

    Installation Modes:
    - PyPI Mode (default): For users who installed 'pip install jamfmcp'
    - Development Mode (--dev): For developers working on JamfMCP source

    All MCP servers run locally via stdio - the distinction is just how
    they're invoked (uvx for PyPI packages vs uv run for development).

    Examples:
        # For users installing from PyPI:
        jamfmcp setup -p claude-desktop --url https://example.jamfcloud.com

        # For developers working on JamfMCP source:
        jamfmcp setup -p claude-desktop --dev --url https://example.jamfcloud.com

        # For Cursor with workspace:
        jamfmcp setup -p cursor --workspace .

        # Dry run to see configuration:
        jamfmcp setup -p gemini-cli --dry-run
    """
    click.echo(click.style(f"\n🚀 Setting up JamfMCP for {platform}\n", fg="cyan", bold=True))

    # Check dependencies
    if not dry_run:
        if not check_uv_installed():
            click.echo(
                click.style(
                    "✗ 'uv' is not installed. Please install it first:\n"
                    "  macOS: brew install uv\n"
                    "  Linux: curl -LsSf https://astral.sh/uv/install.sh | sh",
                    fg="red",
                )
            )
            return

    # Get Jamf URL
    if not url:
        url = await click.prompt("Jamf Pro server URL", type=str)

    # Ensure URL has protocol
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    # Get credentials based on auth type
    credentials = {}
    if not client_id:
        client_id = await click.prompt("Client ID", type=str)
    if not client_secret:
        client_secret = await click.prompt("Client Secret", type=str, hide_input=True)
    credentials = {
        "JAMF_URL": url,
        "JAMF_CLIENT_ID": client_id,
        "JAMF_CLIENT_SECRET": client_secret,
    }

    # Validate connection (unless skipped or dry-run)
    if not skip_validation and not dry_run:
        if verbose:
            click.echo("\nValidating Jamf Pro connection...")
        if await validate_jamf_connection(url, credentials):
            click.echo(click.style("✓ Successfully connected to Jamf Pro", fg="green"))
        else:
            if not click.confirm(
                click.style("Failed to connect to Jamf Pro. Continue anyway?", fg="yellow")
            ):
                return

    # Build MCP configuration file
    mcp_config = build_config(dev=dev, credentials=credentials)

    # Write out config file if requested
    try:
        if write:
            save_mcp_config(mcp_config, platform, workspace)
            click.echo(
                click.style(f"\n✓ Successfully configured {platform}", fg="green", bold=True)
            )
        else:
            click.echo(f"\nJamfMCP Configuration:\n{json.dumps(mcp_config, indent=2)}")

        show_next_steps(platform, workspace)
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        format_err(e)
        sys.exit(1)
