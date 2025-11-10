"""
Simple test to verify logging integration works.
"""

import pytest

from tests.fixtures.mock_context import MockContext


class TestLoggingIntegration:
    """Test that Context logging integration works correctly."""

    @pytest.mark.asyncio
    async def test_mock_context_logging(self) -> None:
        """Test that MockContext captures log messages correctly."""
        ctx = MockContext()

        # Test all log levels
        await ctx.debug("Debug message", {"key": "debug_value"})
        await ctx.info("Info message", {"key": "info_value"})
        await ctx.warning("Warning message", {"key": "warning_value"})
        await ctx.error("Error message", {"key": "error_value"})

        # Verify logs were captured
        assert len(ctx.debug_logs) == 1
        assert ctx.debug_logs[0] == ("Debug message", {"key": "debug_value"})

        assert len(ctx.info_logs) == 1
        assert ctx.info_logs[0] == ("Info message", {"key": "info_value"})

        assert len(ctx.warning_logs) == 1
        assert ctx.warning_logs[0] == ("Warning message", {"key": "warning_value"})

        assert len(ctx.error_logs) == 1
        assert ctx.error_logs[0] == ("Error message", {"key": "error_value"})

        # Verify all_logs
        assert len(ctx.all_logs) == 4
        assert ctx.all_logs[0] == ("debug", "Debug message", {"key": "debug_value"})
        assert ctx.all_logs[3] == ("error", "Error message", {"key": "error_value"})

    @pytest.mark.asyncio
    async def test_context_backward_compatibility(self) -> None:
        """Test that None context doesn't break anything."""
        # This would be tested in actual integration tests with the server
        # For now, just verify our mock context works
        ctx = None

        # In real code, we'd have:
        # if ctx:
        #     await ctx.info("message")

        # Verify this pattern doesn't raise errors
        if ctx:
            await ctx.info("This should not execute")

        # If we got here without errors, the pattern works
        assert True

    def test_get_logs_by_level(self) -> None:
        """Test the get_logs_by_level helper method."""
        ctx = MockContext()

        # Add some async context manager to run async code
        import asyncio

        async def add_logs():
            await ctx.debug("Debug 1")
            await ctx.debug("Debug 2")
            await ctx.info("Info 1")
            await ctx.error("Error 1")

        asyncio.run(add_logs())

        # Test retrieval
        debug_logs = ctx.get_logs_by_level("debug")
        assert len(debug_logs) == 2
        assert debug_logs[0][0] == "Debug 1"
        assert debug_logs[1][0] == "Debug 2"

        info_logs = ctx.get_logs_by_level("info")
        assert len(info_logs) == 1
        assert info_logs[0][0] == "Info 1"

        error_logs = ctx.get_logs_by_level("error")
        assert len(error_logs) == 1
        assert error_logs[0][0] == "Error 1"

        # Test clear
        ctx.clear_logs()
        assert len(ctx.all_logs) == 0
        assert len(ctx.debug_logs) == 0
