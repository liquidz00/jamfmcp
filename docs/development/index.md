# Development Guide

This section covers development practices, architecture details, and contribution guidelines for JamfMCP.

## Development Overview

::::{grid} 2
:gutter: 3

:::{grid-item-card} 🏗️ Architecture
:link: architecture
:link-type: doc

System design and component interactions
:::

:::{grid-item-card} 🤝 Contributing
:link: contributing
:link-type: doc

Guidelines for contributing to JamfMCP
:::

:::{grid-item-card} 🧪 Testing
:link: testing
:link-type: doc

Testing strategies and running tests
:::

:::{grid-item-card} 🚀 Deployment
:link: deployment
:link-type: doc

Deployment options and configurations
:::
::::

## Quick Start for Developers

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp

# Install with dev dependencies
make install-dev

# Run tests
make test

# Check code style
make lint
```

### Development Workflow

1. **Create feature branch**: `git checkout -b feature/your-feature`
2. **Make changes**: Follow code style and add tests
3. **Run tests**: `make test`
4. **Format code**: `make format`
5. **Commit changes**: Use conventional commits
6. **Push and PR**: Create pull request

## Project Structure

```
jamfmcp/
├── src/jamfmcp/          # Source code
│   ├── server.py         # MCP server and tools
│   ├── api.py           # Jamf API client
│   ├── auth.py          # Authentication
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

## Development Principles

### Code Quality

- **Type Hints**: All functions typed
- **Docstrings**: Sphinx-style documentation
- **Testing**: Comprehensive test coverage
- **Linting**: Ruff for style consistency

### Async First

- All API calls are async
- Use `asyncio` patterns
- Handle concurrency properly
- Avoid blocking operations

### Error Handling

- Structured error responses
- Proper logging at all levels
- Graceful degradation
- User-friendly messages

### Security

- No credentials in code
- Secure token handling
- Input validation
- Least privilege principle

## Common Development Tasks

### Adding a New Tool

1. Add tool function to `server.py`
2. Use `@mcp.tool` decorator
3. Add proper type hints
4. Include comprehensive docstring
5. Handle errors appropriately
6. Add tests

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

### Running Tests

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

### Building Documentation

```bash
# Build HTML docs
make docs

# Serve locally
cd docs/_build && python -m http.server
```

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **MacAdmins Slack**: #jamfmcp channel
- **Pull Requests**: Contribute improvements
- **Discussions**: Architecture and design

## Next Steps

- Read the [Architecture Guide](architecture)
- Review [Contributing Guidelines](contributing)
- Explore the [Testing Guide](testing)
- Learn about [Deployment Options](deployment)

:::{seealso}
- [FastMCP Development](https://gofastmcp.com/development/contributing)
- [Python Async Best Practices](https://docs.python.org/3/library/asyncio-dev.html)
- [Pydantic Usage](https://docs.pydantic.dev/)
:::

```{toctree}
:hidden:
:maxdepth: 1

architecture
contributing
testing
deployment
```
