# CHANGELOG

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
* keeping format of `release line`
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


## 0.6.1 - (2017-07-17)
---

### Changed
* add determinism fuzz testing


## 0.6.0 - (2017-07-16)
---

### Added
* add view command


## 0.5.4 - (2017-07-16)
---

### Changed
* add 'keep a changelog' regex for parsing


## 0.5.3 - (2017-06-16)
---

### Fixed
* start first release at 0.1.0


## 0.5.2 - (2017-06-13)
---

### Fixed
* fixing documentation formatting


## 0.5.1 - (2017-06-13)
---

### Fixed
* unreleased position in files with shorter headers


## 0.5.0 - (2017-06-13)
---

### Added
* Added handling for additional version delimiter in changelog files


## 0.4.0 - (2017-06-10)
---

### Added
* added extra line cleanup after release


## 0.3.5 - (2017-06-10)
---

### Changed
* update python versions


## 0.3.4 - (2017-06-10)
---

### Changed
* update test coverage
* add python versions to README.


## 0.3.3 - (2017-06-10)
---

### Changed
* add additional tests
* refactor utils to be classed based for better testing


## 0.3.2 - (2017-06-09)
---

### Fixed
* fix documentation typo


## 0.3.1 - (2017-06-09)
---

### Changed
* adding example changelog output to docs


## 0.3.0 - (2017-06-09)
---

### Added
* added current command

### Changed
* updating documentation


## 0.2.2 - (2017-06-09)
---

### Changed
* update documentation to rst for pypi


## 0.2.1 - (2017-06-09)
---

### Fixed
* version number import


## 0.2.0 - (2017-06-09)
---

### Added
* Add suggest command
* Add version option

### Changed
* changing hardcoded 'CHANGELOG.md' to variable for better mocking in tests
* changing hardcoded  to variable for better mocking in tests
* Updating tests


## 0.1.1 - (2017-06-09)
---

### Changed
* Add README badges
* Add build tools


## 0.1.0 - (2017-06-09)
---

### Added
* Setup initial Project
* Setup Build tools
