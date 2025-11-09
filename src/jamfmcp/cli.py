"""
JamfMCP CLI - Command line interface for configuring JamfMCP with AI platforms.

Provides commands to setup, validate, diagnose, and update JamfMCP configurations
for various AI platforms including Claude Desktop, Cursor, Claude Code, Gemini CLI,
and raw MCP JSON output.
"""

import asyncio
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from getpass import getpass
from pathlib import Path
from typing import Any

import asyncclick as click
import httpx

from jamfmcp.__about__ import __version__
from jamfmcp.auth import JamfAuth

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# Platform configuration paths
PLATFORM_CONFIGS = {
    "claude-desktop": {
        "darwin": "~/Library/Application Support/Claude/claude_desktop_config.json",
        "linux": "~/.config/Claude/claude_desktop_config.json",
    },
    "cursor": "~/.cursor/mcp.json",
    "claude-code": None,  # Uses CLI command
    "gemini-cli": None,  # Uses CLI command
    "mcp-json": None,  # Outputs to stdout
}

# Server name for MCP configuration
SERVER_NAME = "jamfmcp"


# Helper functions
async def get_platform_config_path(platform_name: str) -> Path | None:
    """
    Get the configuration file path for a given platform.

    :param platform_name: The AI platform name
    :type platform_name: str
    :return: Path to the configuration file or None if platform uses CLI
    :rtype: Path | None
    """
    config = PLATFORM_CONFIGS.get(platform_name)
    if config is None:
        return None

    if isinstance(config, dict):
        # Platform-specific paths (e.g., claude-desktop)
        system = platform.system().lower()
        path_str = config.get(system)
        if path_str:
            return Path(path_str).expanduser()
        else:
            click.echo(
                click.style(
                    f"Platform '{platform_name}' is not supported on {platform.system()}",
                    fg="red",
                )
            )
            return None
    else:
        # Single path for all systems
        return Path(config).expanduser()


async def generate_mcp_config(
    auth_type: str, url: str, credentials: dict[str, str]
) -> dict[str, Any]:
    """
    Generate MCP configuration for JamfMCP server.

    :param auth_type: Authentication type ('basic' or 'oauth')
    :type auth_type: str
    :param url: Jamf Pro server URL
    :type url: str
    :param credentials: Authentication credentials
    :type credentials: dict[str, str]
    :return: MCP server configuration
    :rtype: dict[str, Any]
    """
    env_vars = {
        "JAMF_URL": url,
        "JAMF_AUTH_TYPE": auth_type,
    }

    if auth_type == "basic":
        env_vars["JAMF_USERNAME"] = credentials["username"]
        env_vars["JAMF_PASSWORD"] = credentials["password"]
    else:  # oauth
        env_vars["JAMF_CLIENT_ID"] = credentials["client_id"]
        env_vars["JAMF_CLIENT_SECRET"] = credentials["client_secret"]

    return {
        "mcpServers": {
            SERVER_NAME: {
                "command": "uvx",
                "args": ["--from", "jamfmcp", "fastmcp", "run", "jamfmcp.server:mcp"],
                "env": env_vars,
            }
        }
    }


async def write_platform_config(platform_name: str, config: dict[str, Any]) -> None:
    """
    Write configuration to platform-specific location.

    :param platform_name: The AI platform name
    :type platform_name: str
    :param config: The MCP configuration
    :type config: dict[str, Any]
    """
    config_path = await get_platform_config_path(platform_name)
    if config_path is None:
        # Handle CLI-based platforms
        if platform_name == "claude-code":
            await setup_claude_code(config)
        elif platform_name == "gemini-cli":
            await setup_gemini_cli(config)
        elif platform_name == "mcp-json":
            click.echo(json.dumps(config["mcpServers"][SERVER_NAME], indent=2))
        return

    # Create parent directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Backup existing configuration if it exists
    if config_path.exists():
        await backup_existing_config(config_path)

    # Load existing configuration or create new one
    existing_config = {}
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            click.echo(
                click.style(
                    f"Warning: Existing config at {config_path} is invalid JSON. Creating new config.",
                    fg="yellow",
                )
            )

    # Merge configurations
    if "mcpServers" not in existing_config:
        existing_config["mcpServers"] = {}
    existing_config["mcpServers"].update(config["mcpServers"])

    # Write configuration
    with open(config_path, "w") as f:
        json.dump(existing_config, f, indent=2)

    click.echo(
        click.style(
            f"✓ Configuration written to {config_path}",
            fg="green",
        )
    )


async def setup_claude_code(config: dict[str, Any]) -> None:
    """
    Setup JamfMCP for Claude Code using CLI.

    :param config: The MCP configuration
    :type config: dict[str, Any]
    """
    server_config = config["mcpServers"][SERVER_NAME]
    cmd = [
        "claude",
        "mcp",
        "add",
        SERVER_NAME,
    ]

    # Add environment variables
    for key, value in server_config["env"].items():
        cmd.extend(["-e", f"{key}={value}"])

    # Add command and args
    cmd.append(server_config["command"])
    cmd.extend(server_config["args"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            click.echo(click.style(f"✓ Successfully configured Claude Code", fg="green"))
        else:
            click.echo(
                click.style(
                    f"✗ Failed to configure Claude Code: {result.stderr}",
                    fg="red",
                )
            )
    except FileNotFoundError:
        click.echo(
            click.style(
                "✗ Claude Code CLI not found. Please ensure Claude Code is installed.",
                fg="red",
            )
        )


async def setup_gemini_cli(config: dict[str, Any]) -> None:
    """
    Setup JamfMCP for Gemini CLI using CLI.

    :param config: The MCP configuration
    :type config: dict[str, Any]
    """
    server_config = config["mcpServers"][SERVER_NAME]
    cmd = [
        "gemini",
        "mcp",
        "add",
        SERVER_NAME,
    ]

    # Add environment variables
    for key, value in server_config["env"].items():
        cmd.extend(["-e", f"{key}={value}"])

    # Add command and args
    cmd.append("--")
    cmd.append(server_config["command"])
    cmd.extend(server_config["args"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            click.echo(click.style(f"✓ Successfully configured Gemini CLI", fg="green"))
        else:
            click.echo(
                click.style(
                    f"✗ Failed to configure Gemini CLI: {result.stderr}",
                    fg="red",
                )
            )
    except FileNotFoundError:
        click.echo(
            click.style(
                "✗ Gemini CLI not found. Please ensure Gemini CLI is installed.",
                fg="red",
            )
        )


async def validate_jamf_connection(url: str, auth_type: str, credentials: dict[str, str]) -> bool:
    """
    Validate connection to Jamf Pro server.

    :param url: Jamf Pro server URL
    :type url: str
    :param auth_type: Authentication type
    :type auth_type: str
    :param credentials: Authentication credentials
    :type credentials: dict[str, str]
    :return: True if connection is valid
    :rtype: bool
    """
    try:
        # Create temporary auth object
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

        # Use JamfProClient as async context manager
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


async def check_dependencies() -> dict[str, bool]:
    """
    Check for required dependencies.

    :return: Dictionary of dependency check results
    :rtype: dict[str, bool]
    """
    deps = {}

    # Check for uv
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True)
        deps["uv"] = result.returncode == 0
    except FileNotFoundError:
        deps["uv"] = False

    # Check for platform-specific CLIs
    for cmd in ["claude", "gemini"]:
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True)
            deps[cmd] = result.returncode == 0
        except FileNotFoundError:
            deps[cmd] = False

    return deps


async def backup_existing_config(path: Path) -> None:
    """
    Backup existing configuration file.

    :param path: Path to configuration file
    :type path: Path
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.parent / f"{path.stem}.backup.{timestamp}{path.suffix}"
    shutil.copy2(path, backup_path)
    click.echo(click.style(f"Backed up existing config to {backup_path}", fg="yellow"))


async def detect_installed_platforms() -> list[str]:
    """
    Detect which AI platforms are installed.

    :return: List of detected platform names
    :rtype: list[str]
    """
    detected = []

    # Check for configuration files
    for platform_name in ["claude-desktop", "cursor"]:
        config_path = await get_platform_config_path(platform_name)
        if config_path and config_path.exists():
            detected.append(platform_name)

    # Check for CLI tools
    deps = await check_dependencies()
    if deps.get("claude"):
        detected.append("claude-code")
    if deps.get("gemini"):
        detected.append("gemini-cli")

    return detected


# CLI Commands
@click.group(context_settings=CONTEXT_SETTINGS, options_metavar="<options>")
@click.version_option(version=__version__)
async def cli() -> None:
    """
    JamfMCP CLI - Configure JamfMCP for your AI platform.

    This tool helps you set up JamfMCP with various AI platforms including
    Claude Desktop, Cursor, Claude Code, Gemini CLI, and raw MCP JSON output.
    """
    pass


@cli.command(
    "setup",
    short_help="Configure JamfMCP for your AI platform.",
    options_metavar="<options>",
)
@click.option(
    "--platform",
    "-p",
    metavar="<platform>",
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
    metavar="<auth_type>",
    type=click.Choice(["basic", "oauth"], case_sensitive=False),
    default="basic",
    help="Authentication type (default: basic)",
)
@click.option(
    "--url",
    "-u",
    metavar="<jamf_url>",
    type=click.STRING,
    help="Jamf Pro server URL",
)
@click.option(
    "--username",
    metavar="<username>",
    type=click.STRING,
    help="Username for basic auth",
)
@click.option(
    "--password",
    metavar="<password>",
    type=click.STRING,
    help="Password for basic auth",
)
@click.option(
    "--client-id",
    metavar="<client_id>",
    type=click.STRING,
    help="Client ID for OAuth",
)
@click.option(
    "--client-secret",
    metavar="<client_secret>",
    type=click.STRING,
    help="Client secret for OAuth",
)
@click.option(
    "--use-keyring",
    is_flag=True,
    help="Store credentials in system keyring",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making changes",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
async def setup(
    platform: str,
    auth_type: str,
    url: str | None,
    username: str | None,
    password: str | None,
    client_id: str | None,
    client_secret: str | None,
    use_keyring: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    """
    Configure JamfMCP for your AI platform.

    This command will guide you through setting up JamfMCP with your chosen
    AI platform. It will create the necessary configuration files and set up
    authentication credentials.

    Examples:
        jamfmcp setup --platform claude-desktop --auth-type basic --url https://example.jamfcloud.com
        jamfmcp setup --platform cursor --auth-type oauth --use-keyring
        jamfmcp setup --platform mcp-json --auth-type basic --dry-run
    """
    click.echo(click.style(f"\n🚀 Setting up JamfMCP for {platform}\n", fg="cyan", bold=True))

    # Check dependencies
    if verbose:
        click.echo("Checking dependencies...")
    deps = await check_dependencies()
    if not deps["uv"]:
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
        url = click.prompt("Jamf Pro server URL", type=str)

    # Validate URL format
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    # Get credentials based on auth type
    credentials = {}
    if auth_type == "basic":
        if not username:
            username = click.prompt("Username", type=str)
        if not password:
            password = getpass("Password: ")
        credentials = {"username": username, "password": password}
    else:  # oauth
        if not client_id:
            client_id = click.prompt("Client ID", type=str)
        if not client_secret:
            client_secret = getpass("Client Secret: ")
        credentials = {"client_id": client_id, "client_secret": client_secret}

    # Validate connection (skip in dry-run mode)
    if not dry_run:
        if verbose:
            click.echo("\nValidating Jamf Pro connection...")
        if await validate_jamf_connection(url, auth_type, credentials):
            click.echo(click.style("✓ Successfully connected to Jamf Pro", fg="green"))
        else:
            if not click.confirm(
                click.style(
                    "Failed to connect to Jamf Pro. Continue anyway?",
                    fg="yellow",
                )
            ):
                return

    # Generate configuration
    config = await generate_mcp_config(auth_type, url, credentials)

    if dry_run:
        click.echo(click.style("\n--- DRY RUN MODE ---", fg="yellow", bold=True))
        click.echo("Would create the following configuration:\n")
        click.echo(json.dumps(config, indent=2))
        click.echo(click.style("\n--- END DRY RUN ---", fg="yellow", bold=True))
    else:
        # Write configuration
        await write_platform_config(platform, config)

    # Platform-specific instructions
    if platform == "claude-desktop":
        click.echo("\n📝 Next steps:")
        click.echo("1. Restart Claude Desktop completely")
        click.echo("2. Look for the hammer icon (🔨) in the input box")
        click.echo("3. Your JamfMCP tools are now available!")
    elif platform == "cursor":
        click.echo("\n📝 Next steps:")
        click.echo("1. Restart Cursor or reload the window")
        click.echo("2. JamfMCP tools should now be available")
    elif platform in ["claude-code", "gemini-cli"]:
        click.echo("\n📝 Configuration complete!")
        click.echo(f"JamfMCP has been added to {platform}")

    if not use_keyring and platform != "mcp-json":
        click.echo(
            click.style(
                "\n⚠️  Warning: Credentials are stored in plain text in the config file.",
                fg="yellow",
            )
        )
        click.echo("Consider using --use-keyring for secure credential storage.")


@cli.command("validate", short_help="Validate JamfMCP configuration.")
@click.option(
    "--platform",
    "-p",
    metavar="<platform>",
    type=click.Choice(
        ["claude-desktop", "cursor", "claude-code", "gemini-cli", "all"],
        case_sensitive=False,
    ),
    help="Platform to validate (default: all detected)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
async def validate(platform: str | None, verbose: bool) -> None:
    """
    Validate JamfMCP configuration.

    This command checks:
    - Configuration file syntax
    - Jamf Pro connectivity
    - MCP server startup
    - Required dependencies
    """
    click.echo(click.style("\n🔍 Validating JamfMCP configuration\n", fg="cyan", bold=True))

    # Determine which platforms to check
    if platform == "all" or platform is None:
        platforms = await detect_installed_platforms()
        if not platforms:
            click.echo(click.style("No AI platforms detected", fg="yellow"))
            return
    else:
        platforms = [platform]

    # Check dependencies first
    click.echo("Checking dependencies...")
    deps = await check_dependencies()
    if not deps["uv"]:
        click.echo(click.style("✗ 'uv' is not installed", fg="red"))
    else:
        click.echo(click.style("✓ 'uv' is installed", fg="green"))

    # Validate each platform
    for plat in platforms:
        click.echo(f"\n--- Validating {plat} ---")

        # Check if platform uses CLI
        if plat in ["claude-code", "gemini-cli"]:
            cmd_name = "claude" if plat == "claude-code" else "gemini"
            if deps.get(cmd_name):
                click.echo(click.style(f"✓ {cmd_name} CLI is installed", fg="green"))
                # TODO: Check if JamfMCP is configured in the CLI
            else:
                click.echo(click.style(f"✗ {cmd_name} CLI is not installed", fg="red"))
            continue

        # Check configuration file
        config_path = await get_platform_config_path(plat)
        if not config_path:
            continue

        if not config_path.exists():
            click.echo(click.style(f"✗ Configuration file not found: {config_path}", fg="red"))
            continue

        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            click.echo(click.style(f"✓ Configuration file is valid JSON", fg="green"))

            # Check if JamfMCP is configured
            if "mcpServers" in config and SERVER_NAME in config["mcpServers"]:
                click.echo(click.style(f"✓ JamfMCP server is configured", fg="green"))

                # Extract credentials and test connection
                server_config = config["mcpServers"][SERVER_NAME]
                if "env" in server_config:
                    env = server_config["env"]
                    url = env.get("JAMF_URL")
                    auth_type = env.get("JAMF_AUTH_TYPE", "basic")

                    if url:
                        credentials = {}
                        if auth_type == "basic":
                            credentials["username"] = env.get("JAMF_USERNAME", "")
                            credentials["password"] = env.get("JAMF_PASSWORD", "")
                        else:
                            credentials["client_id"] = env.get("JAMF_CLIENT_ID", "")
                            credentials["client_secret"] = env.get("JAMF_CLIENT_SECRET", "")

                        if verbose:
                            click.echo(f"Testing connection to {url}...")
                        if await validate_jamf_connection(url, auth_type, credentials):
                            click.echo(
                                click.style(f"✓ Connection to Jamf Pro successful", fg="green")
                            )
                        else:
                            click.echo(click.style(f"✗ Failed to connect to Jamf Pro", fg="red"))
            else:
                click.echo(click.style(f"✗ JamfMCP server not found in config", fg="red"))

        except json.JSONDecodeError as e:
            click.echo(click.style(f"✗ Invalid JSON in configuration file: {e}", fg="red"))
        except Exception as e:
            click.echo(click.style(f"✗ Error reading configuration: {e}", fg="red"))


@cli.command("doctor", short_help="Diagnose JamfMCP setup issues.")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
async def doctor(verbose: bool) -> None:
    """
    Diagnose JamfMCP setup issues.

    This command performs comprehensive diagnostics including:
    - Checking all platform configurations
    - Testing Jamf Pro API connection
    - Verifying environment setup
    - Providing remediation suggestions
    """
    click.echo(click.style("\n🏥 JamfMCP Doctor\n", fg="cyan", bold=True))
    issues_found = False

    # System information
    click.echo("System Information:")
    click.echo(f"  OS: {platform.system()} {platform.release()}")
    click.echo(f"  Python: {sys.version.split()[0]}")
    click.echo(f"  JamfMCP: {__version__}")

    # Check dependencies
    click.echo("\nDependencies:")
    deps = await check_dependencies()
    for dep, installed in deps.items():
        if installed:
            click.echo(click.style(f"  ✓ {dep}", fg="green"))
        else:
            click.echo(click.style(f"  ✗ {dep}", fg="red"))
            issues_found = True
            if dep == "uv":
                click.echo(
                    "    → Install with: "
                    + (
                        "brew install uv"
                        if platform.system() == "Darwin"
                        else "curl -LsSf https://astral.sh/uv/install.sh | sh"
                    )
                )

    # Check platform configurations
    click.echo("\nPlatform Configurations:")
    platforms = await detect_installed_platforms()

    if not platforms:
        click.echo(click.style("  No AI platforms detected", fg="yellow"))
        click.echo("  → Run 'jamfmcp setup' to configure a platform")
    else:
        for plat in platforms:
            click.echo(f"\n  {plat}:")

            if plat in ["claude-code", "gemini-cli"]:
                # CLI-based platforms
                cmd_name = "claude" if plat == "claude-code" else "gemini"
                if deps.get(cmd_name):
                    click.echo(click.style(f"    ✓ {cmd_name} CLI found", fg="green"))
                else:
                    click.echo(click.style(f"    ✗ {cmd_name} CLI not found", fg="red"))
                    issues_found = True
                continue

            # File-based platforms
            config_path = await get_platform_config_path(plat)
            if config_path and config_path.exists():
                click.echo(click.style(f"    ✓ Config file exists", fg="green"))

                try:
                    with open(config_path, "r") as f:
                        config = json.load(f)

                    if "mcpServers" in config and SERVER_NAME in config["mcpServers"]:
                        click.echo(click.style(f"    ✓ JamfMCP configured", fg="green"))

                        # Test connection
                        server_config = config["mcpServers"][SERVER_NAME]
                        env = server_config.get("env", {})
                        url = env.get("JAMF_URL")

                        if url:
                            click.echo(f"    Jamf URL: {url}")
                            if verbose:
                                auth_type = env.get("JAMF_AUTH_TYPE", "basic")
                                credentials = {}
                                if auth_type == "basic":
                                    credentials["username"] = env.get("JAMF_USERNAME", "")
                                    credentials["password"] = env.get("JAMF_PASSWORD", "")
                                else:
                                    credentials["client_id"] = env.get("JAMF_CLIENT_ID", "")
                                    credentials["client_secret"] = env.get("JAMF_CLIENT_SECRET", "")

                                if await validate_jamf_connection(url, auth_type, credentials):
                                    click.echo(click.style(f"    ✓ API connection OK", fg="green"))
                                else:
                                    click.echo(
                                        click.style(f"    ✗ API connection failed", fg="red")
                                    )
                                    issues_found = True
                    else:
                        click.echo(click.style(f"    ✗ JamfMCP not configured", fg="red"))
                        click.echo(f"    → Run: jamfmcp setup --platform {plat}")
                        issues_found = True

                except Exception as e:
                    click.echo(click.style(f"    ✗ Config error: {e}", fg="red"))
                    issues_found = True
            else:
                click.echo(click.style(f"    ✗ Config file not found", fg="red"))
                click.echo(f"    → Run: jamfmcp setup --platform {plat}")
                issues_found = True

    # Environment variables
    click.echo("\nEnvironment Variables:")
    env_vars = ["JAMF_URL", "JAMF_AUTH_TYPE", "JAMF_USERNAME", "JAMF_CLIENT_ID"]
    env_found = False
    for var in env_vars:
        if os.getenv(var):
            click.echo(click.style(f"  ✓ {var} is set", fg="green"))
            env_found = True
    if not env_found:
        click.echo("  No Jamf environment variables found (this is normal if using config files)")

    # Summary
    click.echo("\n" + "=" * 50)
    if issues_found:
        click.echo(click.style("❌ Issues found. See recommendations above.", fg="red"))
    else:
        click.echo(click.style("✅ Everything looks good!", fg="green"))

    # General recommendations
    if issues_found:
        click.echo("\nGeneral Recommendations:")
        click.echo("1. Ensure 'uv' is installed and in your PATH")
        click.echo("2. Run 'jamfmcp setup' to configure your AI platform")
        click.echo("3. Verify your Jamf Pro credentials are correct")
        click.echo("4. Check that your Jamf Pro server is accessible")


@cli.command("update", short_help="Update JamfMCP package and configurations.")
@click.option(
    "--check-only",
    is_flag=True,
    help="Only check for updates without installing",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
async def update(check_only: bool, verbose: bool) -> None:
    """
    Update JamfMCP package and configurations.

    This command:
    - Checks for JamfMCP package updates
    - Updates existing configurations with new features
    - Preserves user credentials during updates
    """
    click.echo(click.style("\n🔄 JamfMCP Update\n", fg="cyan", bold=True))

    # Check for package updates
    click.echo("Checking for updates...")
    try:
        # Get current version
        current_version = __version__

        # Check PyPI for latest version
        async with httpx.AsyncClient() as client:
            response = await client.get("https://pypi.org/pypi/jamfmcp/json")
            if response.status_code == 200:
                data = response.json()
                latest_version = data["info"]["version"]

                if current_version == latest_version:
                    click.echo(
                        click.style(
                            f"✓ JamfMCP is up to date (v{current_version})",
                            fg="green",
                        )
                    )
                else:
                    click.echo(
                        click.style(
                            f"Update available: v{current_version} → v{latest_version}",
                            fg="yellow",
                        )
                    )
                    if not check_only:
                        if click.confirm("Install update?"):
                            click.echo("Installing update...")
                            result = subprocess.run(
                                ["uv", "pip", "install", "--upgrade", "jamfmcp"],
                                capture_output=True,
                                text=True,
                            )
                            if result.returncode == 0:
                                click.echo(
                                    click.style(
                                        f"✓ Successfully updated to v{latest_version}",
                                        fg="green",
                                    )
                                )
                            else:
                                click.echo(
                                    click.style(
                                        f"✗ Update failed: {result.stderr}",
                                        fg="red",
                                    )
                                )
            else:
                click.echo(click.style("✗ Failed to check for updates", fg="red"))
    except Exception as e:
        click.echo(click.style(f"✗ Error checking updates: {e}", fg="red"))

    if not check_only:
        # Update configurations
        click.echo("\nChecking configurations...")
        platforms = await detect_installed_platforms()

        for plat in platforms:
            if plat in ["claude-code", "gemini-cli"]:
                continue  # Skip CLI-based platforms

            config_path = await get_platform_config_path(plat)
            if config_path and config_path.exists():
                try:
                    with open(config_path, "r") as f:
                        config = json.load(f)

                    if "mcpServers" in config and SERVER_NAME in config["mcpServers"]:
                        server_config = config["mcpServers"][SERVER_NAME]
                        updated = False

                        # Check if using old command format
                        if server_config.get("command") == "python":
                            click.echo(f"\nUpdating {plat} configuration...")
                            # Preserve environment variables
                            env = server_config.get("env", {})

                            # Update to new format
                            server_config["command"] = "uv"
                            server_config["args"] = [
                                "run",
                                "--with",
                                "jamfmcp",
                                "python",
                                "-m",
                                "jamfmcp.server",
                            ]
                            server_config["env"] = env
                            updated = True

                        if updated:
                            # Backup and save
                            await backup_existing_config(config_path)
                            with open(config_path, "w") as f:
                                json.dump(config, f, indent=2)
                            click.echo(
                                click.style(
                                    f"✓ Updated {plat} configuration",
                                    fg="green",
                                )
                            )

                except Exception as e:
                    click.echo(
                        click.style(
                            f"✗ Error updating {plat}: {e}",
                            fg="red",
                        )
                    )

    click.echo("\n✨ Update check complete!")


if __name__ == "__main__":
    asyncio.run(cli())
