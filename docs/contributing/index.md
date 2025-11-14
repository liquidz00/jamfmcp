# Contributing to JamfMCP

Thank you for your interest in contributing to JamfMCP! This guide will help you get started.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git for version control
- GitHub account

## Development Overview

::::{grid} 2
:gutter: 3

:::{grid-item-card} Development Guide
:link: development-guide
:link-type: doc

Configuring your development environment for best success
:::

:::{grid-item-card} 🔐 Security Considerations
:link: security-considerations
:link-type: doc

Security practices to keep in mind when contributing
:::

:::{grid-item-card} 🚀 FastMCP Logging
:link: fastmcp-logging
:link-type: doc

Implementing FastMCP logging mechanisms
:::

:::{grid-item-card} 🧪 Testing
:link: testing
:link-type: doc

Testing strategies and running tests
:::
::::

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

:::{seealso}
- [Support & Resources](../user-guide/support.md)
- [Python Async Best Practices](https://docs.python.org/3/library/asyncio-dev.html)
- [Pydantic Usage](https://docs.pydantic.dev/)
:::

```{toctree}
:caption: Contributing
:hidden:
:maxdepth: 1

development-guide
security-considerations
fastmcp-logging
testing
```
