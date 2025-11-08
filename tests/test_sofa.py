"""
Simple SOFA feed tests.
"""

from jamfmcp.sofa import SOFAFeed, parse_sofa_feed
from tests.fixtures.sofa_data import (
    create_empty_sofa_feed,
    create_sofa_feed_response,
    create_sofa_feed_with_critical_cves,
)


class TestSOFA:
    """Basic SOFA feed parsing tests."""

    def test_parse_sofa_feed_complete(self) -> None:
        """Test parsing a complete SOFA feed."""
        feed_data = create_sofa_feed_response()
        sofa_feed = parse_sofa_feed(feed_data)

        assert isinstance(sofa_feed, SOFAFeed)
        assert sofa_feed.update_hash == feed_data["UpdateHash"]
        assert len(sofa_feed.os_versions) == len(feed_data["OSVersions"])

        # Check that we have some OS versions
        assert len(sofa_feed.os_versions) > 0

        # Check a specific version exists
        version_14_2_1 = sofa_feed.os_versions.get("14.2.1")
        assert version_14_2_1 is not None
        assert version_14_2_1.os_version == "14.2.1"

    def test_parse_sofa_feed_with_cves(self) -> None:
        """Test parsing SOFA feed with CVE data."""
        feed_data = create_sofa_feed_with_critical_cves()
        sofa_feed = parse_sofa_feed(feed_data)

        # Check we have the version with CVEs
        os_version = sofa_feed.os_versions.get("14.0")
        assert os_version is not None

        # Check CVEs were parsed
        assert len(os_version.actively_exploited_cves) > 0

        # Check security releases have CVE data
        if os_version.security_releases:
            first_release = os_version.security_releases[0]
            assert len(first_release.cves) > 0

    def test_parse_empty_sofa_feed(self) -> None:
        """Test parsing an empty SOFA feed."""
        feed_data = create_empty_sofa_feed()
        sofa_feed = parse_sofa_feed(feed_data)

        assert isinstance(sofa_feed, SOFAFeed)
        assert len(sofa_feed.os_versions) == 0
