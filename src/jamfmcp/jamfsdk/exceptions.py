class JamfProSdkException(Exception):
    """Base Jamf Pro SDK Exception"""

    default_message = "An error occurred"

    def __init__(self, message: str = None, **kwargs):
        self.message = message or self.default_message
        self.context = kwargs
        self.formatted_message = self.format_message()
        super().__init__(self.formatted_message)

    def format_message(self) -> str:
        """Format exception message properly."""
        context_details = " | ".join(
            f"{key}: {value}" for key, value in self.context.items() if value
        )
        return f"{self.message} ({context_details})" if context_details else self.message

    def __str__(self):
        return self.formatted_message


class CredentialsError(JamfProSdkException):
    """Credentials Error"""

    pass
