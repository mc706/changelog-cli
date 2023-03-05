# Changelog CLI

[![PyPI version](https://badge.fury.io/py/changelog-cli.svg)](https://badge.fury.io/py/changelog-cli)
[![Build Status](https://github.com/mc706/changelog-cli/workflows/Tests/badge.svg)](https://github.com/mc706/changelog-cli/actions?query=workflow%3ATests)
[![Coverage Status](https://coveralls.io/repos/github/mc706/changelog-cli/badge.svg?branch=master)](https://coveralls.io/github/mc706/changelog-cli?branch=master)
[![PyPI](https://img.shields.io/pypi/pyversions/changelog-cli.svg)](https://pypi.org/project/changelog-cli/)


A command line interface for managing your CHANGELOG.md files. Designed to make it easy to manage your repositories
release history according to [Keep a Changelog](http://keepachangelog.com/) v1.1.0.

## Installation
install using `pip` via:

```
pip install changelog-cli
```


## How To
To keep an accurate changelog, whenever you commit a change that affects how end users use
your project, use this command line tool to add a line to the changelog.

If you added a new feature, use something like `changelog added "added feature x"`. This will add a
line to your `CHANGELOG.md` under the `### Added` section.

When you are ready for release, run `changelog release` and that will infer the correct semantic
version based on the types of changes since the last release. For example your `added` change should
prompt a `minor (0.X.0)` release. A `removed` change would prompt a `major (X.0.0)` version bump and `fixed` or `changed` changes
 would prompt a `patch (0.0.X)`.

You can manually override what type of of release via `changelog release --minor` using the `--patch`, `--minor` or `--major`
flags.


## Commands
`changelog init` -> Creates a CHANGELOG.md with some basic documentation in it.

`changelog (added|changed|deprecated|removed|fixed|security) "<message>"` -> adds a line to the appropriate section

`changelog release (--major|minor|patch|suggest) (--yes)` -> Cuts a release for the changelog, incrementing the version.

`changelog current` -> returns the current version of the project based on the changelog

`changelog suggest` -> returns the suggested version of the next release based on the current logged changes

`changelog --version` -> get the current version of the changelog tool

`changelog --help` -> show helps screen

## Shortcut
If you get tired of typing out `changelog` for every command, it can also be accessed via its shorthand `cl`

## Example Usage
```
>>> changelog current
1.4.1
>>> changelog added "add new feature x"
>>> changelog suggest
1.5.0
>>> changelog removed "removing key feature y"
>>> cl release
Planning on releasing version 2.0.0. Proceed? [y/N]: n
>>> cl release --minor
>>> cl current
1.5.0
```

Example Changelog as a result of the above

```
# CHANGELOG

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

## [1.5.0] - 2017-06-09
---

### Added
* add new feature x

### Removed
* remove key feature y


## [1.4.1] - 2017-05-29
---

### Changed
* updating documentation


...
```
