# Testing Guide

This guide covers testing strategies, patterns, and best practices for JamfMCP.

## Testing Overview

JamfMCP uses pytest for all testing with comprehensive coverage goals:

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

### Test Discovery

pytest automatically discovers tests following these patterns:
- Files: `test_*.py` or `*_test.py`
- Classes: `Test*` (without `__init__` method)
- Functions: `test_*`

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

## Test Patterns

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("valid", {"status": "success"}),
    ("", {"error": "Empty input"}),
    (None, {"error": "None not allowed"}),
    ("special!@#", {"status": "success"}),
])
def test_various_inputs(input, expected):
    """Test function with various inputs."""
    result = function_under_test(input)
    assert result == expected
```

### Testing Exceptions

```python
def test_exception_handling():
    """Test that function raises expected exception."""
    with pytest.raises(ValueError) as exc_info:
        function_that_should_fail()

    assert "Invalid input" in str(exc_info.value)

@pytest.mark.asyncio
async def test_async_exception():
    """Test async exception handling."""
    with pytest.raises(JamfApiError):
        await async_function_that_fails()
```

### Testing Logging

```python
def test_logging(caplog):
    """Test that function logs correctly."""
    with caplog.at_level(logging.ERROR):
        function_with_logging()

    assert "Error message" in caplog.text
    assert caplog.records[0].levelname == "ERROR"
```

## Integration Testing

### Testing with Real Services

```python
@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("JAMF_URL"),
    reason="Jamf credentials not configured"
)
async def test_real_api_call():
    """Test with real Jamf Pro API."""
    auth = JamfAuth()
    api = JamfApi(auth)

    result = await api.get_computer_inventory("REAL_SERIAL")
    assert "general" in result
```

### Testing Tool Integration

```python
@pytest.mark.asyncio
async def test_tool_integration(mock_jamf_api, mock_sofa_feed):
    """Test complete tool flow."""
    # Setup mocks
    mock_jamf_api.get_computer_inventory.return_value = inventory_data
    mock_jamf_api.get_computer_history.return_value = history_data

    # Test tool
    result = await get_health_scorecard(serial="ABC123")

    # Verify integration
    assert result["overall_score"] > 0
    assert result["grade"] in ["A", "B", "C", "D", "F"]
```

## Test Data Management

### Using Fixtures for Test Data

```python
# In fixtures/computer_data.py
def get_sample_computer():
    """Get sample computer data."""
    return {
        "general": {
            "id": 123,
            "name": "Test Mac",
            "serial_number": "ABC123"
        }
    }

# In test file
from fixtures.computer_data import get_sample_computer

def test_with_sample_data():
    """Test using sample data."""
    computer = get_sample_computer()
    result = process_computer(computer)
    assert result is not None
```

### Factory Pattern

```python
class ComputerFactory:
    """Factory for creating test computers."""

    @staticmethod
    def create(name="Test Mac", **kwargs):
        """Create test computer with defaults."""
        computer = {
            "general": {
                "name": name,
                "serial_number": "ABC123",
                "id": 123
            }
        }
        computer.update(kwargs)
        return computer

# Usage
def test_with_factory():
    """Test using factory."""
    computer = ComputerFactory.create(name="Custom Mac")
    assert computer["general"]["name"] == "Custom Mac"
```

## Coverage

### Coverage Configuration

In `pyproject.toml`:

```toml
[tool.coverage.run]
omit = [
    "src/jamfmcp/jamfsdk/*",  # Exclude SDK
    "*/tests/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

### Coverage Goals

- **Overall**: 90%+ coverage
- **Core Modules**: 95%+ coverage
- **New Code**: 100% coverage
- **Exclude**: Generated code, SDK

### Viewing Coverage

```bash
# Terminal report
make test-cov

# HTML report
make test-cov-html
open htmlcov/index.html
```

## Best Practices

### Test Independence

```python
# Bad - tests depend on order
class TestDependent:
    shared_state = []

    def test_first(self):
        self.shared_state.append(1)

    def test_second(self):
        assert len(self.shared_state) == 1  # Fails if run alone

# Good - independent tests
class TestIndependent:
    def test_first(self):
        state = []
        state.append(1)
        assert len(state) == 1

    def test_second(self):
        state = [1]
        assert len(state) == 1
```

### Clear Test Names

```python
# Bad
def test_1():
    pass

def test_function():
    pass

# Good
def test_health_scorecard_returns_valid_grade():
    pass

def test_invalid_serial_raises_value_error():
    pass
```

### Arrange-Act-Assert Pattern

```python
@pytest.mark.asyncio
async def test_get_computer_inventory():
    """Test getting computer inventory."""
    # Arrange
    serial = "ABC123"
    expected_data = {"general": {"name": "Test Mac"}}
    mock_api.return_value = expected_data

    # Act
    result = await get_computer_inventory(serial)

    # Assert
    assert result == expected_data
    mock_api.assert_called_once_with(serial=serial)
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

## Performance Testing

### Timing Tests

```python
@pytest.mark.timeout(5)
def test_performance():
    """Test completes within 5 seconds."""
    result = potentially_slow_function()
    assert result is not None
```

### Benchmark Tests

```python
def test_benchmark(benchmark):
    """Benchmark function performance."""
    result = benchmark(function_to_benchmark, arg1, arg2)
    assert result is not None
```

:::{seealso}
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [pytest-mock](https://github.com/pytest-dev/pytest-mock)
- [Coverage.py](https://coverage.readthedocs.io/)
:::
