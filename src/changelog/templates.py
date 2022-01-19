BASE = """# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).
"""

DEFAULT_VERSION = "0.0.0"

RELEASE_LINE = "## [{}] - ({})\n"

RELEASE_LINE_REGEXES = [
    r"^##\s\[(?P<v>\d+\.\d+\.\d+)\]\s\-\s\(\d{4}-\d{2}-\d{2}\)$",
    r"##\s\[v?(?P<v>\d+\.\d+\.\d+)\]",
    r"^##\s\[(?P<v>\d+\.\d+\.\d+)\]\s\-\s\d{4}-\d{2}-\d{2}$",
]
