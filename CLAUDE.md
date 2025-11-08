# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **jamfmcp**, an async MCP (Model Context Protocol) server for Jamf Pro integration. It provides tools for computer health analysis, inventory management, and policy monitoring through the Jamf Pro API. The project uses FastMCP to expose Jamf Pro functionality to AI assistants.

## Development Commands

### Setup and Installation
```bash
make install-dev          # Install project with dev dependencies
make venv                 # Create virtual environment only
```

### Testing
```bash
make test                 # Run all tests with verbose output
make test-cov             # Run tests with coverage report
make test-cov-html        # Generate HTML coverage report
uv run pytest tests/ -v   # Direct pytest invocation
uv run pytest tests/test_auth.py -v  # Run specific test file
```

Note: The `jamfsdk` directory is excluded from test discovery and coverage reporting.

### Code Quality
```bash
make lint                 # Check code style with ruff (format + lint)
make format               # Auto-format code with ruff
make pre-commit           # Install pre-commit hooks
make pre-commit-run       # Run pre-commit on all files
```

### Dependency Management
```bash
make lock                 # Update uv.lock file
make upgrade              # Upgrade all dependencies to latest versions
```

### Building
```bash
make build                # Build wheel and sdist packages
```

### Cleanup
```bash
make clean                # Remove build artifacts and cache files
make flush                # Deep clean (all generated files)
make restore              # Full cleanup (clean + flush)
```

## Architecture

### Core Components

1. **MCP Server (`server.py`)**: FastMCP-based server exposing tools for Jamf Pro API interaction. All tools are async and handle ID parameters as strings or integers for MCP client compatibility.

2. **API Client (`api.py`)**: `JamfApi` class wraps the underlying `JamfProClient` from jamfsdk. Provides high-level async methods for:
   - Computer inventory and history
   - User and device lookups
   - Policy and configuration profile management
   - JCDS (Jamf Cloud Distribution Service) operations
   - Organizational data (buildings, departments, sites, network segments)

3. **Authentication (`auth.py`)**: `JamfAuth` class supports two authentication methods:
   - Basic auth (username/password) via `UserCredentialsProvider`
   - OAuth client credentials via `ApiClientCredentialsProvider`
   - Reads from environment variables: `JAMF_URL`, `JAMF_USERNAME`, `JAMF_PASSWORD`, `JAMF_CLIENT_ID`, `JAMF_CLIENT_SECRET`, `JAMF_AUTH_TYPE`
   - Automatically strips whitespace and parses URLs to extract FQDN

4. **Health Analyzer (`health_analyzer.py`)**: Generates comprehensive health scorecards for managed computers by analyzing:
   - Security compliance (FileVault, Gatekeeper, SIP, XProtect, Firewall)
   - OS currency and CVE vulnerabilities (via SOFA feed integration)
   - Policy execution and management history
   - Hardware and system diagnostics
   - Returns structured health scores (A-F grades) with recommendations

5. **SOFA Integration (`sofa.py`)**: Integrates with macadmins SOFA feed for macOS security intelligence:
   - CVE tracking and actively exploited vulnerabilities
   - OS version currency analysis
   - Security update recommendations

6. **Jamf SDK (`src/jamfmcp/jamfsdk/`)**: Embedded SDK for Jamf Pro API interaction with:
   - Pydantic models for Pro and Classic API responses
   - Async HTTP client with automatic pagination
   - Support for both Pro API (v1/v2) and Classic API endpoints
   - JCDS and webhook support

### Key Design Patterns

- **Async-first**: All API operations use `async`/`await` with `httpx.AsyncClient`
- **Context managers**: `JamfProClient` uses `async with` for automatic session management
- **Error handling**: Structured error responses as dictionaries with `error` and `message` keys
- **Type safety**: Extensive use of Pydantic models and Python 3.13 type hints
- **ID flexibility**: MCP tools accept IDs as `str | int` since some clients serialize numbers as strings

## Code Style Requirements

### Python Reference
Always use `python3` explicitly in commands, not `python` (per global CLAUDE.md).

### Docstring Format
Use **Sphinx/reStructuredText style only** (enforced by `.cursor/rules/sphinx-style-docstrings.mdc`):
```python
def example(param: str, count: int = 10) -> dict[str, Any]:
    """
    Short description.

    Longer description if needed.

    :param param: Parameter description
    :type param: str
    :param count: Count parameter with default
    :type count: int
    :return: Return value description
    :rtype: dict[str, Any]
    :raises ValueError: When validation fails
    """
```

**Never use Google or NumPy docstring styles.**

### Type Hints
- Use modern Python 3.10+ syntax: `str | None` instead of `Optional[str]`
- Use built-in generics: `list[str]`, `dict[str, int]`, `tuple[int, ...]`
- Import from `typing` only for: `Any`, `TypeVar`, `Literal`, `Callable`, `Protocol`, `TypedDict`

### Code Formatting
- Max line length: 100 characters
- Use `ruff` for formatting and linting
- Follow PEP 8: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants

### Async Development
Write async code by default for:
- All API requests
- File or network I/O
- Concurrent operations
Use `httpx.AsyncClient` (not `requests`). Only use synchronous code when required by third-party libraries or CLI wrappers.

## Testing

- Framework: `pytest` with `pytest-asyncio`, `pytest-cov`, `pytest-mock`
- Test files in `tests/` directory parallel to `src/`
- Fixtures in `tests/fixtures/` for shared test data
- Mock external API calls in unit tests
- Run single test: `uv run pytest tests/test_auth.py::test_function_name -v`

## Environment Variables

Required for MCP server operation:
- `JAMF_URL`: Jamf Pro server URL (FQDN or full URL)
- `JAMF_AUTH_TYPE`: "basic" or "client_credentials" (default: "basic")

For basic auth:
- `JAMF_USERNAME`: Jamf Pro username
- `JAMF_PASSWORD`: Jamf Pro password

For OAuth:
- `JAMF_CLIENT_ID`: OAuth client ID
- `JAMF_CLIENT_SECRET`: OAuth client secret

## Important Notes

- The `jamfsdk/` directory is an embedded SDK and is excluded from test coverage
- MCP tools accept ID parameters as strings to accommodate JSON schema validation across clients
- Error responses from tools are dicts with `error`, `message`, and context keys (e.g., `serial`, `computer_id`)
- Health scorecard generation requires SOFA feed access; gracefully degrades if unavailable
- Pagination is handled automatically by the SDK's `FilterField` and `get_computer_inventory_v1` methods
