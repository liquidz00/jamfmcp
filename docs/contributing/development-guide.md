# Development Guide

Configuring your development environment for best success

## Project Structure

```
jamfmcp/
├── src/jamfmcp/          # Source code
│   ├── server.py         # MCP server and tools
│   ├── api.py           # Jamf API client
│   ├── auth.py          # Authentication
│   ├── cli.py          # CLI entry point
│   ├── health_analyzer.py # Health analysis
│   ├── sofa.py          # SOFA integration
│   └── jamfsdk/         # Embedded SDK
├── tests/               # Test suite
│   ├── conftest.py      # Pytest configuration
│   ├── fixtures/        # Test data
│   └── test_*.py        # Test modules
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
└── Makefile            # Development tasks
```

## Key Technologies

- **Python 3.13+**: Modern Python features
- **FastMCP**: MCP server framework
- **httpx**: Async HTTP client
- **Pydantic**: Data validation
- **pytest**: Testing framework
- **Sphinx**: Documentation
- **uv**: Package management

## Development Workflow

### 1. Create Feature Branch

1. **Fork the repository** on GitHub
2. **Clone your fork**: `git clone https://github.com/YOUR_USERNAME/jamfmcp.git && cd jamfmcp`
3. **Add upstream remote**: `git remote add upstream https://github.com/liquidz00/jamfmcp.git`
4. **Install development dependencies**: `make install-dev`
5. **Create a feature branch**: `git checkout -b feature/your-feature-name`

:::{tip}
All `make` commands are configured to use `uv`. You do not need to worry about creating a virtual environment for dependency installation as this is all handled automatically by `uv`. To see a list of all available commands in the Makefile, see [Makefile commands](#makefile_commands)
:::

### 2. Make Your Changes

Follow these guidelines:

- **Code Style**: Follow existing patterns
- **Type Hints**: Add type hints to all functions
- **Docstrings**: Use Sphinx-style docstrings

:::{dropdown} Example DocString
:open:
```python
async def get_example_data(
    item_id: str,
    include_details: bool = False
) -> dict[str, Any]:
    """
    Get example data from Jamf Pro.

    This function retrieves example data with optional details.

    :param item_id: The unique identifier for the item
    :type item_id: str
    :param include_details: Whether to include additional details
    :type include_details: bool
    :return: Dictionary containing the example data
    :rtype: dict[str, Any]
    :raises ValueError: If item_id is invalid
    :raises JamfApiError: If API call fails
    """
    # Implementation
```
:::

#### Building Documentation

```bash
# Build HTML docs
make docs

# Serve locally
cd docs/_build && python -m http.server
```

### 3. Creating and Running Tests

Write comprehensive tests for your changes:

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_get_example_data_success(mock_jamf_api):
    """Test successful data retrieval."""
    # Arrange
    mock_jamf_api.get_example.return_value = {
        "id": "123",
        "name": "Test Item"
    }

    # Act
    result = await get_example_data("123")

    # Assert
    assert result["id"] == "123"
    assert result["name"] == "Test Item"
    mock_jamf_api.get_example.assert_called_once_with("123", details=False)

@pytest.mark.asyncio
async def test_get_example_data_invalid_id():
    """Test handling of invalid ID."""
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid ID"):
        await get_example_data("")
```

#### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Specific test file
uv run pytest tests/test_health_analyzer.py

# Specific test
uv run pytest tests/test_health_analyzer.py::test_score_calculation
```

:::{seealso}
See the full [testing guide](#testing) for more on writing unit tests.
:::

### 4. Format and Lint Code

We use Ruff for code formatting and linting:

```bash
# Format code
make format

# Check style
make lint
```

#### Style Guidelines

- **Line Length**: Maximum 100 characters
- **Imports**: Use absolute imports
- **Naming**: Follow PEP 8 conventions
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### 5. Commit Your Changes

Use conventional commit messages:

```bash
# Format: <type>(<scope>): <subject>

feat(tools): add new inventory search tool
fix(auth): handle token expiration correctly
docs(readme): update installation instructions
test(health): add tests for CVE analysis
refactor(api): simplify error handling
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Maintenance tasks

### 6. Push and Create Pull Request (PR)

1. **Push to your fork**: `git push origin feature/your-feature-name`
2. **Create Pull Request** on GitHub
3. **Fill out PR template** completely
4. **Link related issues** if applicable

## Pull Request Guidelines

### PR Checklist

- [ ] Tests pass locally (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Documentation is updated
- [ ] PR description is complete

## Review Process

### What to Expect

1. **Initial Review**: Maintainers review code changes and/or documentation updates
2. **Feedback**: Address requested changes
3. **CI Checks**: Ensure all checks pass
4. **Approval**: Maintainer approval required
5. **Merge**: Maintainer merges PR

### Review Criteria

- **Code Quality**: Clean, readable, maintainable
- **Tests**: Comprehensive test coverage
- **Documentation**: Clear and complete
- **Performance**: No performance regressions
- **Security**: No security vulnerabilities

(makefile_commands)=
## Makefile Commands

:::note
In order to use `make` commands on macOS you must install [Xcode Command Line Tools](https://mac.install.guide/commandlinetools/)
:::

To view all command options, execute `make help`:
```
Available commands:

  Installation & Setup:
    make venv             - Create virtual environment
    make install          - Install base dependencies
    make install-dev      - Install dev dependencies (includes docs)
    make uninstall        - Remove virtual environment
    make sync             - Alias for 'make install'

  Development:
    make lint             - Check code style with ruff
    make format           - Auto-format code with ruff
    make pre-commit       - Install pre-commit hooks
    make pre-commit-run   - Run pre-commit on all files
    make pre-commit-update - Update pre-commit hooks to latest versions

  Testing:
    make test             - Run all tests (verbose)
    make test-cov         - Run tests with coverage report
    make test-cov-html    - Generate HTML coverage report

  Building & Documentation:
    make build            - Build distribution packages (wheel & sdist)
    make docs             - Build Sphinx documentation

  Dependency Management:
    make lock             - Update uv.lock file
    make upgrade          - Upgrade all dependencies to latest versions

  Cleanup:
    make clean            - Remove build artifacts and cache files
    make flush            - Deep clean (remove all generated files)
    make restore          - Full cleanup (clean + flush)
```

## Common Development Tasks

### Adding a New Tool

1. Add tool function to `server.py`
2. Use `@mcp.tool` decorator
3. Add proper type hints
4. Include comprehensive docstring
5. Handle errors appropriately

Example:
```python
@mcp.tool
async def get_new_data(
    param: str,
    optional: bool = False
) -> dict[str, Any]:
    """
    Get new data from Jamf Pro.

    :param param: Required parameter
    :type param: str
    :param optional: Optional flag
    :type optional: bool
    :return: Data dictionary
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_new_data(param, optional)
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}
```

### Adding Health Checks

1. Extend Health Analysis in `src/jamfmcp/health_analyzer.py`
2. Add scoring logic, allow for configurable weight scoring
3. Include recommendations for remediation or troubleshooting
4. Update unit tests in `tests/test_health_analyzer.py`

### Custom Analyzers

```python
class CustomAnalyzer(HealthAnalyzer):
    def _calculate_custom_score(self) -> HealthScore:
        # Custom scoring logic
        pass
```

## Recognition

Contributors are recognized in:
- CHANGELOG.md for their contributions
- GitHub contributors page
- Release notes

Thank you for contributing to JamfMCP! 🎉
