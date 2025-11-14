(testing)=
# Testing Guide

This guide covers testing strategies, patterns, and best practices for JamfMCP.

## Testing Overview

JamfMCP uses pytest for all testing with the following goals in mind:

- **Unit Tests**: Individual components
- **Integration Tests**: Component interactions
- **Async Tests**: Async function testing
- **Mock Testing**: External service mocking

## Running Tests

### Basic Commands

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Generate HTML coverage report
make test-cov-html

# Run specific test file
uv run pytest tests/test_health_analyzer.py

# Run specific test
uv run pytest tests/test_health_analyzer.py::test_generate_scorecard

# Run with verbose output
uv run pytest -v

# Run with print statements
uv run pytest -s
```

## Test Structure

### Project Test Layout

```
tests/
├── __init__.py              # Makes tests a package
├── conftest.py             # Shared fixtures and configuration
├── fixtures/               # Test data fixtures
│   ├── __init__.py
│   ├── api_responses.py    # Mock API responses
│   ├── computer_data.py    # Sample computer data
│   └── sofa_data.py        # SOFA feed samples
├── test_auth.py            # Authentication tests
├── test_health_analyzer.py # Health analyzer tests
├── test_mcp_tools.py       # MCP tool tests
└── test_sofa.py            # SOFA integration tests
```

### Test File Structure

```python
"""Test module for feature name."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from jamfmcp.module import FeatureClass


class TestFeatureName:
    """Test suite for FeatureName."""

    @pytest.fixture
    def feature_instance(self):
        """Create feature instance for testing."""
        return FeatureClass()

    def test_basic_functionality(self, feature_instance):
        """Test basic feature functionality."""
        result = feature_instance.do_something()
        assert result == expected_value

    @pytest.mark.asyncio
    async def test_async_functionality(self, feature_instance):
        """Test async feature functionality."""
        result = await feature_instance.async_method()
        assert result["status"] == "success"
```

## Fixtures

### Built-in Fixtures

JamfMCP provides common fixtures in `conftest.py`:

```python
@pytest.fixture
def sample_computer_inventory():
    """Provide sample computer inventory data."""
    return {
        "general": {
            "id": 123,
            "name": "Test Computer",
            "serial_number": "ABC123"
        },
        "hardware": {
            "make": "Apple",
            "model": "MacBook Pro"
        }
    }

@pytest.fixture
def mock_jamf_api(mocker):
    """Mock JamfApi for testing."""
    return mocker.patch('jamfmcp.server.jamf_api')

@pytest.fixture
def mock_sofa_feed():
    """Provide mock SOFA feed data."""
    return SOFAFeed(
        update_hash="test123",
        os_versions={"Sonoma 14": OSVersionInfo(...)}
    )
```

### Using Fixtures

```python
def test_with_fixtures(sample_computer_inventory, mock_jamf_api):
    """Test using multiple fixtures."""
    # Fixtures are automatically injected
    mock_jamf_api.get_computer_inventory.return_value = sample_computer_inventory

    result = some_function()
    assert result["general"]["name"] == "Test Computer"
```

### Custom Fixtures

```python
@pytest.fixture(scope="function")  # Default scope
def custom_data():
    """Provide custom test data."""
    data = {"key": "value"}
    yield data  # Provide to test
    # Cleanup if needed

@pytest.fixture(scope="module")
def expensive_resource():
    """Create expensive resource once per module."""
    resource = create_expensive_resource()
    yield resource
    resource.cleanup()
```

## Async Testing

### Testing Async Functions

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await async_function()
    assert result == expected

@pytest.mark.asyncio
async def test_multiple_async_calls():
    """Test multiple async operations."""
    results = await asyncio.gather(
        async_function1(),
        async_function2()
    )
    assert len(results) == 2
```

### Async Fixtures

```python
@pytest.fixture
async def async_client():
    """Provide async client."""
    client = AsyncClient()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """Test using async fixture."""
    result = await async_client.get_data()
    assert result is not None
```

## Mocking

### Mocking External Services

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock_api(mocker):
    """Test with mocked API calls."""
    # Mock the API client
    mock_api = mocker.patch('jamfmcp.api.JamfApi')
    mock_api.get_computer_inventory = AsyncMock(return_value={
        "general": {"name": "Test Mac"}
    })

    # Test the function
    result = await function_under_test()

    # Verify mock was called
    mock_api.get_computer_inventory.assert_called_once_with(serial="ABC123")
```

### Mock Patterns

```python
# Mock return value
mock.return_value = {"data": "value"}

# Mock async return
mock.return_value = AsyncMock(return_value={"data": "value"})

# Mock side effect
mock.side_effect = [result1, result2, Exception("Error")]

# Mock property
type(mock).property_name = PropertyMock(return_value="value")

# Partial mock
with patch.object(instance, 'method', return_value="mocked"):
    result = instance.method()
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Pull requests
- Push to main branch
- Nightly scheduled runs

### Pre-commit Hooks

```bash
# Install hooks
make pre-commit

# Run manually
make pre-commit-run
```

## Debugging Tests

### Using pdb

```python
def test_with_debugger():
    """Test with debugger."""
    import pdb; pdb.set_trace()
    result = complex_function()
    assert result is not None
```

### Verbose Output

```bash
# Show print statements
pytest -s

# Show test names as they run
pytest -v

# Show local variables on failure
pytest -l
```

### Test Isolation

```bash
# Run single test
pytest tests/test_file.py::test_name

# Run tests matching pattern
pytest -k "test_health"

# Run marked tests
pytest -m "slow"
```

:::{seealso}
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [pytest-mock](https://github.com/pytest-dev/pytest-mock)
- [Coverage.py](https://coverage.readthedocs.io/)
:::
