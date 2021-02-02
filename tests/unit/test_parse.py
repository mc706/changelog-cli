import unittest
from typing import Iterable

from changelog.parser import parse


class ParseTestCase(unittest.TestCase):
    def test_happy_path(self):
        stream = parse(iter(SAMPLE.split('\n')))
        self.assertTrue(isinstance(stream, Iterable))
        unwound = list(stream)
        self.assertEqual(len(unwound), 3)
        self.assertEqual(unwound[0]['version'], 'Unreleased')

    def test_empty_file(self):
        empty_response = next(parse(iter(())), None)
        self.assertIsNone(empty_response)

    def test_new_file(self):
        stream = parse(iter(NEW_SAMPLE.split('\n')))
        self.assertTrue(isinstance(stream, Iterable))
        unwound = list(stream)
        self.assertEqual(len(unwound), 1)

    def test_doesnt_read_in_full_file_when_not_needed(self):
        stream = parse(iter(SAMPLE.split('\n')))
        unreleased = next(stream)
        self.assertEqual(unreleased['version'], 'Unreleased')
        v7 = next(stream)
        self.assertEqual(v7['version'], '0.7.0')
        self.assertIsNotNone(next(stream, None))

SAMPLE = """# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).

## Unreleased
---

### Added
* Added the new CLI flags for the Changelog v1.1 change types
  * `--added`, `--changed`, `--deprecated`, `--removed`, `--fixed`, `--security`
  
### Changed
* Switched the change type headers in "Unreleased" to match Keep A Changelog v1.1's headers
  * Existing CHANGELOGs will start using these headers after the new run of `changelog release`

### Fixed
* Fix Description for pypi

### Removed
* Removed support for Python 2
* Removed support for Python 3 prior to 3.6
* Removed the previous CLI flags for the change type headers: `--new`, `--change`, `--fix`, `--breaks`

## 0.7.0 - (2020-02-09)
---

### Added
* Expose the type of release with `changelog suggest --type`


## 0.6.2 - (2017-10-27)
---

### Fixed
* update init template


"""

NEW_SAMPLE = """# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).

## Unreleased
---

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

"""
