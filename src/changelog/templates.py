BASE = """# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).
"""

DEFAULT_VERSION = "0.0.0"

RELEASE_LINE = {
    "date": "## {} - ({})\n",
    "pure": "## {}\n",
    "bracket_date": "## [{}] - {}\n"
}

RELEASE_LINE_REGEXES = {
    "date": r"^##\s(?P<v>\d+\.\d+\.\d+)\s\-\s\(\d{4}-\d{2}-\d{2}\)$",
    "pure": r"^##\sv?(?P<v>\d+\.\d+\.\d+)",
    "bracket_date": r"^##\s\[(?P<v>\d+\.\d+\.\d+)\]\s\-\s\d{4}-\d{2}-\d{2}$"
}
