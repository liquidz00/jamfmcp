"""
Simple MCP tools tests - just verify core logic works.
"""

from tests.fixtures.computer_data import create_healthy_computer


class TestMCPTools:
    """Basic MCP tools tests - verify the core logic works."""

    def test_health_scorecard_generation(self) -> None:
        """Test the health scorecard generation logic."""
        from jamfmcp.health_analyzer import HealthAnalyzer, HealthScorecard

        computer_data = create_healthy_computer()
        analyzer = HealthAnalyzer(computer_data)

        scorecard = analyzer.generate_health_scorecard()

        assert isinstance(scorecard, HealthScorecard)
        assert hasattr(scorecard, "overall_score")
        assert isinstance(scorecard.overall_score, (int, float))
        assert 0 <= scorecard.overall_score <= 100

    def test_sofa_feed_parsing(self) -> None:
        """Test SOFA feed parsing logic."""
        from jamfmcp.sofa import SOFAFeed, parse_sofa_feed
        from tests.fixtures.sofa_data import create_sofa_feed_response

        feed_data = create_sofa_feed_response()
        parsed_feed = parse_sofa_feed(feed_data)

        assert isinstance(parsed_feed, SOFAFeed)
        assert len(parsed_feed.os_versions) > 0
