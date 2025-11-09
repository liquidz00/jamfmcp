# Contributing to JamfMCP

Thank you for your interest in contributing to JamfMCP! This guide will help you get started.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git for version control
- GitHub account

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/jamfmcp.git
   cd jamfmcp
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/liquidz00/jamfmcp.git
   ```

4. **Install development dependencies**:
   ```bash
   make install-dev
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### 1. Make Your Changes

Follow these guidelines:

- **Code Style**: Follow existing patterns
- **Type Hints**: Add type hints to all functions
- **Docstrings**: Use Sphinx-style docstrings
- **Tests**: Add tests for new functionality

### 2. Code Style

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

### 3. Documentation

All code must be documented:

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

    Example:
        >>> data = await get_example_data("123", include_details=True)
        >>> print(data["name"])
    """
    # Implementation
```

### 4. Testing

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

Run tests:
```bash
# All tests
make test

# With coverage
make test-cov

# Specific test
uv run pytest tests/test_your_feature.py -v
```

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

### 6. Push and Create PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub
3. **Fill out PR template** completely
4. **Link related issues** if applicable

## Pull Request Guidelines

### PR Checklist

- [ ] Tests pass locally (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] PR description is complete

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Fixes #123
```

## Adding New Features

### Adding a New MCP Tool

1. **Add tool function** to `src/jamfmcp/server.py`:
   ```python
   @mcp.tool
   async def get_new_feature(
       param: str,
       optional: bool = False
   ) -> dict[str, Any]:
       """
       Get new feature data.

       :param param: Required parameter
       :type param: str
       :param optional: Optional flag
       :type optional: bool
       :return: Feature data
       :rtype: dict[str, Any]
       """
       try:
           return await jamf_api.get_new_feature(param, optional)
       except Exception as e:
           logger.error(f"Error getting feature: {e}")
           return {"error": str(e)}
   ```

2. **Add API method** if needed in `src/jamfmcp/api.py`

3. **Write tests** in `tests/test_mcp_tools.py`

4. **Update documentation** in `docs/tools/`

### Adding Health Checks

1. **Extend HealthAnalyzer** in `src/jamfmcp/health_analyzer.py`
2. **Add scoring logic** with appropriate weights
3. **Include recommendations**
4. **Update tests**

## Testing Guidelines

### Test Structure

```python
class TestFeatureName:
    """Test suite for feature name."""

    @pytest.fixture
    def setup_data(self):
        """Provide test data."""
        return {"test": "data"}

    async def test_success_case(self, setup_data):
        """Test successful operation."""
        # Test implementation

    async def test_error_case(self):
        """Test error handling."""
        # Test implementation

    @pytest.mark.parametrize("input,expected", [
        ("valid", {"result": "success"}),
        ("", {"error": "Invalid input"}),
    ])
    async def test_various_inputs(self, input, expected):
        """Test various input scenarios."""
        # Test implementation
```

### Mock Best Practices

```python
@pytest.fixture
def mock_jamf_api(mocker):
    """Mock JamfApi for testing."""
    mock = mocker.patch('jamfmcp.server.jamf_api')
    # Configure mock behavior
    return mock
```

## Documentation

### Adding Documentation

1. **API Documentation**: Add to `docs/api-reference/`
2. **Tool Documentation**: Add to `docs/tools/`
3. **User Guides**: Update relevant guides
4. **Examples**: Include usage examples

### Documentation Style

- Use MyST Markdown
- Include code examples
- Add cross-references
- Keep it concise and clear

## Review Process

### What to Expect

1. **Initial Review**: Maintainers review within 3-5 days
2. **Feedback**: Address requested changes
3. **CI Checks**: Ensure all checks pass
4. **Approval**: Two approvals required
5. **Merge**: Maintainer merges PR

### Review Criteria

- **Code Quality**: Clean, readable, maintainable
- **Tests**: Comprehensive test coverage
- **Documentation**: Clear and complete
- **Performance**: No performance regressions
- **Security**: No security vulnerabilities

## Release Process

1. **Version Bump**: Update version in `__about__.py`
2. **Changelog**: Update CHANGELOG.md
3. **Tag Release**: Create version tag
4. **Build**: Create distribution packages
5. **Publish**: Upload to PyPI (maintainers only)

## Getting Help

### Resources

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions and share ideas
- **MacAdmins Slack**: Join #jamfmcp channel
- **Documentation**: Read the docs thoroughly

### Asking Questions

When asking for help:
1. Search existing issues first
2. Provide context and examples
3. Include error messages
4. Specify versions used

## Recognition

Contributors are recognized in:
- CHANGELOG.md for their contributions
- GitHub contributors page
- Release notes

Thank you for contributing to JamfMCP! 🎉

:::{seealso}
- [Development Setup](index)
- [Architecture Guide](architecture)
- [Testing Guide](testing)
- [Python Style Guide](https://peps.python.org/pep-0008/)
:::
