"""
Mock Context for testing FastMCP logging.
"""

from typing import Any


class MockContext:
    """
    Mock implementation of FastMCP Context for testing.

    This mock captures all log messages for verification in tests.
    """

    def __init__(self) -> None:
        """
        Initialize the mock context with empty log lists.
        """
        self.debug_logs: list[tuple[str, dict[str, Any] | None]] = []
        self.info_logs: list[tuple[str, dict[str, Any] | None]] = []
        self.warning_logs: list[tuple[str, dict[str, Any] | None]] = []
        self.error_logs: list[tuple[str, dict[str, Any] | None]] = []
        self.all_logs: list[tuple[str, str, dict[str, Any] | None]] = []

    async def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        Capture debug log messages.

        :param message: The debug message
        :type message: str
        :param extra: Optional extra data for structured logging
        :type extra: dict[str, Any] | None
        """
        self.debug_logs.append((message, extra))
        self.all_logs.append(("debug", message, extra))

    async def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        Capture info log messages.

        :param message: The info message
        :type message: str
        :param extra: Optional extra data for structured logging
        :type extra: dict[str, Any] | None
        """
        self.info_logs.append((message, extra))
        self.all_logs.append(("info", message, extra))

    async def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        Capture warning log messages.

        :param message: The warning message
        :type message: str
        :param extra: Optional extra data for structured logging
        :type extra: dict[str, Any] | None
        """
        self.warning_logs.append((message, extra))
        self.all_logs.append(("warning", message, extra))

    async def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        Capture error log messages.

        :param message: The error message
        :type message: str
        :param extra: Optional extra data for structured logging
        :type extra: dict[str, Any] | None
        """
        self.error_logs.append((message, extra))
        self.all_logs.append(("error", message, extra))

    async def log(
        self,
        level: str,
        message: str,
        logger_name: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """
        Capture generic log messages.

        :param level: The log level
        :type level: str
        :param message: The log message
        :type message: str
        :param logger_name: Optional logger name
        :type logger_name: str | None
        :param extra: Optional extra data for structured logging
        :type extra: dict[str, Any] | None
        """
        # Route to appropriate level method
        if level == "debug":
            await self.debug(message, extra)
        elif level == "info":
            await self.info(message, extra)
        elif level == "warning":
            await self.warning(message, extra)
        elif level == "error":
            await self.error(message, extra)

    def get_logs_by_level(self, level: str) -> list[tuple[str, dict[str, Any] | None]]:
        """
        Get all logs for a specific level.

        :param level: The log level to retrieve
        :type level: str
        :return: List of (message, extra) tuples for the specified level
        :rtype: list[tuple[str, dict[str, Any] | None]]
        """
        if level == "debug":
            return self.debug_logs
        elif level == "info":
            return self.info_logs
        elif level == "warning":
            return self.warning_logs
        elif level == "error":
            return self.error_logs
        else:
            return []

    def clear_logs(self) -> None:
        """
        Clear all captured logs.
        """
        self.debug_logs.clear()
        self.info_logs.clear()
        self.warning_logs.clear()
        self.error_logs.clear()
        self.all_logs.clear()
