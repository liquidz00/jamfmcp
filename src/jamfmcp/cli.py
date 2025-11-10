"""
JamfMCP CLI - Simplified wrapper for configuring JamfMCP with AI platforms.

This CLI helps users set up JamfMCP by collecting Jamf credentials and calling
fastmcp install with the appropriate environment variables.
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

import asyncclick as click

from jamfmcp.__about__ import __version__
from jamfmcp.auth import JamfAuth

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


async def validate_jamf_connection(url: str, auth_type: str, credentials: dict[str, str]) -> bool:
    """
    Validate connection to Jamf Pro server.

    :param url: Jamf Pro server URL
    :type url: str
    :param auth_type: Authentication type ('basic' or 'oauth')
    :type auth_type: str
    :param credentials: Authentication credentials
    :type credentials: dict[str, str]
    :return: True if connection is valid
    :rtype: bool
    """
    try:
        # Create auth object
        if auth_type == "basic":
            auth = JamfAuth(
                auth_type=auth_type,
                server=url,
                username=credentials["username"],
                password=credentials["password"],
            )
        else:  # oauth
            auth = JamfAuth(
                auth_type=auth_type,
                server=url,
                client_id=credentials["client_id"],
                client_secret=credentials["client_secret"],
            )

        # Test connection
        from jamfmcp.jamfsdk import JamfProClient

        async with JamfProClient(
            server=auth.server, credentials=auth.get_credentials_provider()
        ) as client:
            # Simple API call to verify connection
            response = await client.pro_api_request("get", "/api/v1/auth")
            return response.status_code == 200
    except Exception as e:
        click.echo(click.style(f"Connection failed: {str(e)}", fg="red"))
        return False


def check_fastmcp_installed() -> bool:
    """
    Check if FastMCP CLI is installed.

    :return: True if FastMCP is installed
    :rtype: bool
    """
    try:
        result = subprocess.run(["fastmcp", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
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


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
async def cli() -> None:
    """
    JamfMCP CLI - Configure JamfMCP for your AI platform.

    This tool helps you set up JamfMCP with various AI platforms including
    Claude Desktop, Cursor, Claude Code, Gemini CLI, and MCP JSON output.
    """
    pass


@cli.command("setup", short_help="Configure JamfMCP for your AI platform.")
@click.option(
    "--platform",
    "-p",
    type=click.Choice(
        ["claude-desktop", "cursor", "claude-code", "gemini-cli", "mcp-json"],
        case_sensitive=False,
    ),
    required=True,
    help="AI platform to configure",
)
@click.option(
    "--auth-type",
    "-a",
    type=click.Choice(["basic", "oauth"], case_sensitive=False),
    default="basic",
    help="Authentication type (default: basic)",
)
@click.option(
    "--url",
    "-u",
    type=str,
    help="Jamf Pro server URL",
)
@click.option(
    "--username",
    type=str,
    help="Username for basic auth",
)
@click.option(
    "--password",
    type=str,
    help="Password for basic auth",
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
    "--server-name",
    "-n",
    type=str,
    default="jamfmcp",
    help="Custom name for the server (default: jamfmcp)",
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
    "--local",
    "-l",
    is_flag=True,
    help="Use local editable installation instead of PyPi package",
)
async def setup(
    platform: str,
    auth_type: str,
    url: str | None,
    username: str | None,
    password: str | None,
    client_id: str | None,
    client_secret: str | None,
    workspace: Path | None,
    server_name: str,
    skip_validation: bool,
    verbose: bool,
    dry_run: bool,
    local: bool,
) -> None:
    """
    Configure JamfMCP for your AI platform.

    This command collects your Jamf Pro credentials and uses FastMCP's install
    command to set up JamfMCP with your chosen AI platform.

    Examples:
        jamfmcp setup -p claude-desktop --url https://example.jamfcloud.com
        jamfmcp setup -p cursor --auth-type oauth --workspace .
        jamfmcp setup -p mcp-json --dry-run
    """
    click.echo(click.style(f"\n🚀 Setting up JamfMCP for {platform}\n", fg="cyan", bold=True))

    # Check dependencies
    if not dry_run:
        if not check_fastmcp_installed():
            click.echo(
                click.style(
                    "✗ FastMCP is not installed. Please install it first:\n  pip install fastmcp",
                    fg="red",
                )
            )
            return

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
    if auth_type == "basic":
        if not username:
            username = await click.prompt("Username", type=str)
        if not password:
            password = await click.prompt("Password", type=str, hide_input=True)
        credentials = {"username": username, "password": password}
    else:  # oauth
        if not client_id:
            client_id = await click.prompt("Client ID", type=str)
        if not client_secret:
            client_secret = await click.prompt("Client Secret", type=str, hide_input=True)
        credentials = {"client_id": client_id, "client_secret": client_secret}

    # Validate connection (unless skipped or dry-run)
    if not skip_validation and not dry_run:
        if verbose:
            click.echo("\nValidating Jamf Pro connection...")
        if await validate_jamf_connection(url, auth_type, credentials):
            click.echo(click.style("✓ Successfully connected to Jamf Pro", fg="green"))
        else:
            if not click.confirm(
                click.style("Failed to connect to Jamf Pro. Continue anyway?", fg="yellow")
            ):
                return

    # Build FastMCP install command
    if local:
        import jamfmcp

        # Use actual filepath for local development
        module_path = os.path.dirname(jamfmcp.__file__)
        server_path = os.path.join(module_path, "server.py")
        cmd = ["fastmcp", "install", platform, f"{server_path}:mcp"]
        cmd.extend(["--server-name", server_name])
        project_root = os.path.dirname(os.path.dirname(module_path))
        cmd.extend(["--with-editable", project_root])
    else:
        cmd = ["fastmcp", "install", platform, "jamfmcp.server:mcp"]
        cmd.extend(["--server-name", server_name])
        # Add jamfmcp package as dependency
        cmd.extend(["--with", "jamfmcp"])

    # Add environment variables
    cmd.extend(["--env", f"JAMF_URL={url}"])
    cmd.extend(["--env", f"JAMF_AUTH_TYPE={auth_type}"])

    if auth_type == "basic":
        cmd.extend(["--env", f"JAMF_USERNAME={credentials['username']}"])
        cmd.extend(["--env", f"JAMF_PASSWORD={credentials['password']}"])
    else:  # oauth
        cmd.extend(["--env", f"JAMF_CLIENT_ID={credentials['client_id']}"])
        cmd.extend(["--env", f"JAMF_CLIENT_SECRET={credentials['client_secret']}"])

    # Add workspace for Cursor if specified
    if platform == "cursor" and workspace:
        cmd.extend(["--workspace", str(workspace)])

    # Execute or show command
    if dry_run:
        click.echo(click.style("\n--- DRY RUN MODE ---", fg="yellow", bold=True))
        click.echo("Would execute the following command:\n")
        # Mask sensitive information in dry-run output
        safe_cmd = []
        skip_next = False
        for i, arg in enumerate(cmd):
            if skip_next:
                skip_next = False
                continue
            if arg == "--env" and i + 1 < len(cmd):
                # Check if next arg contains sensitive data
                env_var = cmd[i + 1]
                if "PASSWORD=" in env_var or "SECRET=" in env_var:
                    # Mask the value part
                    key = env_var.split("=")[0]
                    safe_cmd.append(arg)
                    safe_cmd.append(f"{key}=***")
                else:
                    safe_cmd.append(arg)
                    safe_cmd.append(env_var)
                skip_next = True
            else:
                safe_cmd.append(arg)
        click.echo(f"  {' '.join(safe_cmd)}")
        click.echo(click.style("\n--- END DRY RUN ---", fg="yellow", bold=True))
    else:
        if verbose:
            # Show command with masked credentials
            safe_cmd = []
            skip_next = False
            for i, arg in enumerate(cmd):
                if skip_next:
                    skip_next = False
                    continue
                if arg == "--env" and i + 1 < len(cmd):
                    # Check if next arg contains sensitive data
                    env_var = cmd[i + 1]
                    if "PASSWORD=" in env_var or "SECRET=" in env_var:
                        # Mask the value part
                        key = env_var.split("=")[0]
                        safe_cmd.append(arg)
                        safe_cmd.append(f"{key}=***")
                    else:
                        safe_cmd.append(arg)
                        safe_cmd.append(env_var)
                    skip_next = True
                else:
                    safe_cmd.append(arg)
            click.echo(f"Running: {' '.join(safe_cmd)}\n")

        # Execute the command
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                click.echo(
                    click.style(f"\n✓ Successfully configured {platform}", fg="green", bold=True)
                )

                # Platform-specific instructions
                if platform == "claude-desktop":
                    click.echo("\n📝 Next steps:")
                    click.echo("1. Restart Claude Desktop completely")
                    click.echo("2. Look for the hammer icon (🔨) in the input box")
                    click.echo("3. Your JamfMCP tools are now available!")
                elif platform == "cursor":
                    if workspace:
                        click.echo("\n📝 Next steps:")
                        click.echo(f"1. Open Cursor in workspace: {workspace}")
                        click.echo("2. JamfMCP tools should now be available")
                    else:
                        click.echo("\n📝 Next steps:")
                        click.echo("1. Click 'Install' in the Cursor prompt")
                        click.echo("2. Restart Cursor or reload the window")
                        click.echo("3. JamfMCP tools should now be available")
                elif platform == "claude-code":
                    click.echo("\n📝 Configuration complete!")
                    click.echo("JamfMCP has been added to Claude Code")
                elif platform == "gemini-cli":
                    click.echo("\n📝 Configuration complete!")
                    click.echo("JamfMCP has been added to Gemini CLI")
                elif platform == "mcp-json":
                    click.echo("\n📝 MCP JSON configuration generated!")
                    if result.stdout:
                        click.echo("\n" + result.stdout)
            else:
                click.echo(click.style(f"✗ Failed to configure {platform}", fg="red", bold=True))
                if result.stderr:
                    click.echo(click.style(f"Error: {result.stderr}", fg="red"))
                if verbose and result.stdout:
                    click.echo(f"Output: {result.stdout}")
        except FileNotFoundError:
            click.echo(
                click.style(
                    "✗ FastMCP CLI not found. Please install it with: pip install fastmcp",
                    fg="red",
                )
            )
        except Exception as e:
            click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))


@cli.command("validate", short_help="Validate Jamf Pro connection.")
@click.option(
    "--auth-type",
    "-a",
    type=click.Choice(["basic", "oauth"], case_sensitive=False),
    default="basic",
    help="Authentication type (default: basic)",
)
@click.option(
    "--url",
    "-u",
    type=str,
    help="Jamf Pro server URL",
)
@click.option(
    "--username",
    type=str,
    help="Username for basic auth",
)
@click.option(
    "--password",
    type=str,
    help="Password for basic auth",
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
async def validate(
    auth_type: str,
    url: str | None,
    username: str | None,
    password: str | None,
    client_id: str | None,
    client_secret: str | None,
) -> None:
    """
    Validate Jamf Pro connection with provided credentials.

    This command tests the connection to your Jamf Pro server to ensure
    the credentials are correct before setting up JamfMCP.

    Examples:
        jamfmcp validate --url https://example.jamfcloud.com
        jamfmcp validate --auth-type oauth --url https://example.jamfcloud.com
    """
    click.echo(click.style("\n🔍 Validating Jamf Pro Connection\n", fg="cyan", bold=True))

    # Get Jamf URL
    if not url:
        url = await click.prompt("Jamf Pro server URL", type=str)

    # Ensure URL has protocol
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    # Get credentials based on auth type
    credentials = {}
    if auth_type == "basic":
        if not username:
            username = await click.prompt("Username", type=str)
        if not password:
            password = await click.prompt("Password", type=str, hide_input=True)
        credentials = {"username": username, "password": password}
    else:  # oauth
        if not client_id:
            client_id = await click.prompt("Client ID", type=str)
        if not client_secret:
            client_secret = await click.prompt("Client Secret", type=str, hide_input=True)
        credentials = {"client_id": client_id, "client_secret": client_secret}

    # Validate connection
    click.echo("\nTesting connection...")
    if await validate_jamf_connection(url, auth_type, credentials):
        click.echo(click.style("✓ Successfully connected to Jamf Pro!", fg="green", bold=True))
        click.echo(f"  Server: {url}")
        click.echo(f"  Auth Type: {auth_type}")
    else:
        click.echo(click.style("✗ Failed to connect to Jamf Pro", fg="red", bold=True))
        click.echo("\nPlease check:")
        click.echo("  • Server URL is correct")
        click.echo("  • Credentials are valid")
        click.echo("  • User has API access permissions")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(cli())
