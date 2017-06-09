BASE = """# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/)."""

UNRELEASED = """
## Unreleased
---

### New

### Changes

### Fixes

### Breaks


"""

INIT = BASE + UNRELEASED

DEFAULT_VERSION = "0.1.0"

RELEASE_LINE = "## {0} - ({1})\n"

RELEASE_LINE_REGEX = r"^## (\d+\.\d+\.\d+) \- \(\d{4}-\d{2}-\d{2}\)$"
