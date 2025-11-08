"""
SOFA feed test data fixtures.

This module provides mock SOFA (Simple Organized Feed for Apple software updates)
data including CVE vulnerability information for testing health analysis.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

faker = Faker()


def create_sofa_feed_response() -> dict[str, Any]:
    """
    Create a comprehensive mock SOFA feed response.

    :return: Mock SOFA feed data
    :rtype: dict[str, Any]
    """
    return {
        "UpdateHash": faker.sha256(),
        "OSVersions": [
            {
                "OSVersion": "14.2.1",
                "Latest": {
                    "ProductVersion": "14.2.1",
                    "Build": "23C71",
                    "ReleaseDate": "2023-12-11T18:00:00Z",
                    "ExpirationDate": "2024-12-11T18:00:00Z",
                    "SupportedDevices": [
                        "Mac14,7",
                        "Mac15,3",
                        "Mac15,6",
                        "Mac15,7",
                        "Mac15,8",
                        "Mac15,9",
                    ],
                    "CVEs": {
                        "CVE-2023-42940": False,
                        "CVE-2023-42941": False,
                        "CVE-2023-42942": True,
                        "CVE-2023-42943": False,
                    },
                    "ActivelyExploitedCVEs": ["CVE-2023-42942"],
                    "UniqueCVEsCount": 4,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Sonoma 14.2.1",
                        "ProductVersion": "14.2.1",
                        "ReleaseDate": "2023-12-11T18:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT214036",
                        "CVEs": {
                            "CVE-2023-42940": False,
                            "CVE-2023-42941": False,
                            "CVE-2023-42942": True,
                            "CVE-2023-42943": False,
                        },
                        "ActivelyExploitedCVEs": ["CVE-2023-42942"],
                        "UniqueCVEsCount": 4,
                    }
                ],
            },
            {
                "OSVersion": "14.2",
                "Latest": {
                    "ProductVersion": "14.2",
                    "Build": "23C64",
                    "ReleaseDate": "2023-12-05T18:00:00Z",
                    "ExpirationDate": "2024-12-05T18:00:00Z",
                    "SupportedDevices": [
                        "Mac14,7",
                        "Mac15,3",
                        "Mac15,6",
                        "Mac15,7",
                        "Mac15,8",
                        "Mac15,9",
                    ],
                    "CVEs": {
                        "CVE-2023-42890": False,
                        "CVE-2023-42891": False,
                        "CVE-2023-42892": False,
                        "CVE-2023-42893": False,
                        "CVE-2023-42894": False,
                    },
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 5,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Sonoma 14.2",
                        "ProductVersion": "14.2",
                        "ReleaseDate": "2023-12-05T18:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT214035",
                        "CVEs": {
                            "CVE-2023-42890": False,
                            "CVE-2023-42891": False,
                            "CVE-2023-42892": False,
                            "CVE-2023-42893": False,
                            "CVE-2023-42894": False,
                        },
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 5,
                    }
                ],
            },
            {
                "OSVersion": "14.1.2",
                "Latest": {
                    "ProductVersion": "14.1.2",
                    "Build": "23B92",
                    "ReleaseDate": "2023-11-30T18:00:00Z",
                    "ExpirationDate": "2024-11-30T18:00:00Z",
                    "SupportedDevices": ["Mac14,7", "Mac15,3", "Mac15,6", "Mac15,7"],
                    "CVEs": {
                        "CVE-2023-42916": True,
                        "CVE-2023-42917": True,
                    },
                    "ActivelyExploitedCVEs": ["CVE-2023-42916", "CVE-2023-42917"],
                    "UniqueCVEsCount": 2,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Sonoma 14.1.2",
                        "ProductVersion": "14.1.2",
                        "ReleaseDate": "2023-11-30T18:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT214032",
                        "CVEs": {
                            "CVE-2023-42916": True,
                            "CVE-2023-42917": True,
                        },
                        "ActivelyExploitedCVEs": ["CVE-2023-42916", "CVE-2023-42917"],
                        "UniqueCVEsCount": 2,
                    }
                ],
            },
            {
                "OSVersion": "14.1.1",
                "Latest": {
                    "ProductVersion": "14.1.1",
                    "Build": "23B81",
                    "ReleaseDate": "2023-11-07T18:00:00Z",
                    "ExpirationDate": "2024-11-07T18:00:00Z",
                    "SupportedDevices": ["Mac14,7", "Mac15,3", "Mac15,6", "Mac15,7"],
                    "CVEs": {},
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 0,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Sonoma 14.1.1",
                        "ProductVersion": "14.1.1",
                        "ReleaseDate": "2023-11-07T18:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT213984",
                        "CVEs": {},
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 0,
                    }
                ],
            },
            {
                "OSVersion": "14.1",
                "Latest": {
                    "ProductVersion": "14.1",
                    "Build": "23B74",
                    "ReleaseDate": "2023-10-25T17:00:00Z",
                    "ExpirationDate": "2024-10-25T17:00:00Z",
                    "SupportedDevices": ["Mac14,7", "Mac15,3", "Mac15,6", "Mac15,7"],
                    "CVEs": {
                        "CVE-2023-41974": False,
                        "CVE-2023-41975": False,
                        "CVE-2023-41976": False,
                    },
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 3,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Sonoma 14.1",
                        "ProductVersion": "14.1",
                        "ReleaseDate": "2023-10-25T17:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT213931",
                        "CVEs": {
                            "CVE-2023-41974": False,
                            "CVE-2023-41975": False,
                            "CVE-2023-41976": False,
                        },
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 3,
                    }
                ],
            },
            {
                "OSVersion": "13.6.3",
                "Latest": {
                    "ProductVersion": "13.6.3",
                    "Build": "22G436",
                    "ReleaseDate": "2023-12-11T18:00:00Z",
                    "ExpirationDate": "2024-12-11T18:00:00Z",
                    "SupportedDevices": [
                        "MacBookPro16,1",
                        "MacBookPro16,2",
                        "MacBookPro16,3",
                        "MacBookPro16,4",
                    ],
                    "CVEs": {
                        "CVE-2023-42940": False,
                        "CVE-2023-42941": False,
                    },
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 2,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Ventura 13.6.3",
                        "ProductVersion": "13.6.3",
                        "ReleaseDate": "2023-12-11T18:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT214036",
                        "CVEs": {
                            "CVE-2023-42940": False,
                            "CVE-2023-42941": False,
                        },
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 2,
                    }
                ],
            },
            {
                "OSVersion": "12.7.2",
                "Latest": {
                    "ProductVersion": "12.7.2",
                    "Build": "21H1015",
                    "ReleaseDate": "2023-12-11T18:00:00Z",
                    "ExpirationDate": "2024-12-11T18:00:00Z",
                    "SupportedDevices": [
                        "MacBookPro15,1",
                        "MacBookPro15,2",
                        "MacBookPro15,3",
                        "MacBookPro15,4",
                    ],
                    "CVEs": {"CVE-2023-42940": False},
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 1,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Monterey 12.7.2",
                        "ProductVersion": "12.7.2",
                        "ReleaseDate": "2023-12-11T18:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT214037",
                        "CVEs": {"CVE-2023-42940": False},
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 1,
                    }
                ],
            },
            {
                "OSVersion": "12.6.1",
                "Latest": {
                    "ProductVersion": "12.6.1",
                    "Build": "21G217",
                    "ReleaseDate": "2022-10-24T17:00:00Z",
                    "ExpirationDate": "2023-10-24T17:00:00Z",
                    "SupportedDevices": [
                        "MacBookPro15,1",
                        "MacBookPro15,2",
                        "MacBookPro15,3",
                        "MacBookPro15,4",
                    ],
                    "CVEs": {"CVE-2022-42827": False},
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 1,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Monterey 12.6.1",
                        "ProductVersion": "12.6.1",
                        "ReleaseDate": "2022-10-24T17:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT213488",
                        "CVEs": {"CVE-2022-42827": False},
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 1,
                    }
                ],
            },
        ],
    }


def create_minimal_sofa_feed() -> dict[str, Any]:
    """
    Create a minimal SOFA feed response for testing.

    :return: Minimal SOFA feed data
    :rtype: dict[str, Any]
    """
    return {
        "UpdateHash": faker.sha256(),
        "OSVersions": [
            {
                "OSVersion": "14.2.1",
                "Latest": {
                    "ProductVersion": "14.2.1",
                    "Build": "23C71",
                    "ReleaseDate": "2023-12-11T18:00:00Z",
                    "CVEs": {},
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 0,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Sonoma 14.2.1",
                        "ProductVersion": "14.2.1",
                        "ReleaseDate": "2023-12-11T18:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT214036",
                        "CVEs": {},
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 0,
                    }
                ],
            }
        ],
    }


def create_sofa_feed_with_critical_cves() -> dict[str, Any]:
    """
    Create a SOFA feed with critical actively exploited CVEs.

    :return: SOFA feed with critical CVEs
    :rtype: dict[str, Any]
    """
    return {
        "UpdateHash": faker.sha256(),
        "OSVersions": [
            {
                "OSVersion": "14.0",
                "Latest": {
                    "ProductVersion": "14.0",
                    "Build": "23A344",
                    "ReleaseDate": "2023-09-26T17:00:00Z",
                    "CVEs": {
                        "CVE-2023-41064": True,
                        "CVE-2023-41061": True,
                        "CVE-2023-41059": True,
                        "CVE-2023-41058": True,
                        "CVE-2023-41056": True,
                    },
                    "ActivelyExploitedCVEs": [
                        "CVE-2023-41064",
                        "CVE-2023-41061",
                        "CVE-2023-41059",
                        "CVE-2023-41058",
                        "CVE-2023-41056",
                    ],
                    "UniqueCVEsCount": 5,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Sonoma 14.0",
                        "ProductVersion": "14.0",
                        "ReleaseDate": "2023-09-26T17:00:00Z",
                        "SecurityInfo": "https://support.apple.com/en-us/HT213893",
                        "CVEs": {
                            "CVE-2023-41064": True,
                            "CVE-2023-41061": True,
                            "CVE-2023-41059": True,
                            "CVE-2023-41058": True,
                            "CVE-2023-41056": True,
                        },
                        "ActivelyExploitedCVEs": [
                            "CVE-2023-41064",
                            "CVE-2023-41061",
                            "CVE-2023-41059",
                            "CVE-2023-41058",
                            "CVE-2023-41056",
                        ],
                        "UniqueCVEsCount": 5,
                    }
                ],
            }
        ],
    }


def create_sofa_feed_for_os_version(
    os_version: str, build: str, cve_count: int = 3, actively_exploited_count: int = 0
) -> dict[str, Any]:
    """
    Create a SOFA feed for a specific OS version.

    :param os_version: macOS version
    :type os_version: str
    :param build: Build number
    :type build: str
    :param cve_count: Number of CVEs to generate
    :type cve_count: int
    :param actively_exploited_count: Number of actively exploited CVEs
    :type actively_exploited_count: int
    :return: SOFA feed data
    :rtype: dict[str, Any]
    """
    cves = {}
    exploited_cves = []
    for i in range(cve_count):
        cve_id = f"CVE-2023-{faker.random_int(min=40000, max=49999)}"
        is_exploited = i < actively_exploited_count
        cves[cve_id] = is_exploited
        if is_exploited:
            exploited_cves.append(cve_id)

    release_date = faker.date_time_this_year().isoformat() + "Z"
    return {
        "UpdateHash": faker.sha256(),
        "OSVersions": [
            {
                "OSVersion": os_version,
                "Latest": {
                    "ProductVersion": os_version,
                    "Build": build,
                    "ReleaseDate": release_date,
                    "CVEs": cves,
                    "ActivelyExploitedCVEs": exploited_cves,
                    "UniqueCVEsCount": cve_count,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": f"macOS Update {os_version}",
                        "ProductVersion": os_version,
                        "ReleaseDate": release_date,
                        "SecurityInfo": f"https://support.apple.com/en-us/HT{faker.random_int(min=210000, max=219999)}",
                        "CVEs": cves,
                        "ActivelyExploitedCVEs": exploited_cves,
                        "UniqueCVEsCount": cve_count,
                    }
                ],
            }
        ],
    }


def create_empty_sofa_feed() -> dict[str, Any]:
    """
    Create an empty SOFA feed response.

    :return: Empty SOFA feed data
    :rtype: dict[str, Any]
    """
    return {"UpdateHash": faker.sha256(), "OSVersions": []}


def create_sofa_feed_with_future_dates() -> dict[str, Any]:
    """
    Create a SOFA feed with future release dates for testing.

    :return: SOFA feed with future dates
    :rtype: dict[str, Any]
    """
    future_date = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    return {
        "UpdateHash": faker.sha256(),
        "OSVersions": [
            {
                "OSVersion": "15.0",
                "Latest": {
                    "ProductVersion": "15.0",
                    "Build": "24A100",
                    "ReleaseDate": future_date,
                    "CVEs": {},
                    "ActivelyExploitedCVEs": [],
                    "UniqueCVEsCount": 0,
                },
                "SecurityReleases": [
                    {
                        "UpdateName": "macOS Future 15.0",
                        "ProductVersion": "15.0",
                        "ReleaseDate": future_date,
                        "SecurityInfo": "https://support.apple.com/en-us/HT999999",
                        "CVEs": {},
                        "ActivelyExploitedCVEs": [],
                        "UniqueCVEsCount": 0,
                    }
                ],
            }
        ],
    }


def create_cve_details() -> dict[str, Any]:
    """
    Create detailed CVE information.

    :return: CVE details
    :rtype: dict[str, Any]
    """
    return {
        "CVE": f"CVE-2023-{faker.random_int(min=40000, max=49999)}",
        "Description": faker.text(max_nb_chars=200),
        "Severity": faker.random_element(["Critical", "High", "Medium", "Low"]),
        "CVSS": faker.pyfloat(min_value=0.0, max_value=10.0, right_digits=1),
        "AffectedComponent": faker.random_element(
            ["WebKit", "Kernel", "Safari", "Mail", "Messages"]
        ),
        "Impact": faker.random_element(
            [
                "Arbitrary code execution",
                "Privilege escalation",
                "Information disclosure",
                "Denial of service",
            ]
        ),
        "ActivelyExploitedInTheWild": faker.boolean(chance_of_getting_true=20),
    }
