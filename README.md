# Changelog CLI

[![PyPI version](https://badge.fury.io/py/changelog-cli.svg)](https://badge.fury.io/py/changelog-cli)
[![Build Status](https://travis-ci.org/mc706/changelog-cli.svg?branch=master)](https://travis-ci.org/mc706/changelog-cli)
[![Code Health](https://landscape.io/github/mc706/changelog-cli/master/landscape.svg?style=flat)](https://landscape.io/github/mc706/changelog-cli/master)
[![Coverage Status](https://coveralls.io/repos/github/mc706/changelog-cli/badge.svg?branch=master)](https://coveralls.io/github/mc706/changelog-cli?branch=master)
[![PyPI](https://img.shields.io/pypi/pyversions/changelog-cli.svg)](https://pypi.org/project/changelog-cli/)
[![Stories in Ready](https://badge.waffle.io/mc706/changelog-cli.png?label=ready&title=Ready)](https://waffle.io/mc706/changelog-cli?utm_source=badge)


A command line interface for managing your CHANGELOG.md files. Designed to make it easy to manage your repositories
release history according to [Keep a Changelog](http://keepachangelog.com/).

## Installation
install using `pip` via:

```
pip install changelog-cli
```


## How To
To keep an accurate changelog, whenenever you commit a change that affects how end users use
your project, use this command line tool to add a line to the changelog. 

If you added a new feature, use something like `changelog new "added feature x"`. This will add a
line to your `CHANGELOG.md` under the `### New` section. 

When you are ready for release, run `changelog release` and that will infer the correct semantic 
version based on the types of changes since the last release. For example your `new` change should
prompt a `minor (0.X.0)` release. A `breaks` change would prompt a `major (X.0.0)` version bump and `fix` or `change` changes
 would prompt a `patch (0.0.X)`.
 
You can manually override what type of of release via `changelog release --minor` using the `--patch`, `--minor` or `--major`
flags. 


## Commands
`changelog init` -> Creates a CHANGELOG.md with some basic documentation in it.

`changelog (new|change|fix|breaks) "<message>"` -> adds a line to the appropriate section

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
>>> changelog new "add new feature x"
>>> changelog suggest
1.5.0
>>> changelog breaks "removing key feature y"
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

### New

### Changes

### Fixes

### Breaks


## 1.5.0 - (2017-06-09)
---

### New
* add new feature x

### Breaks
* remove key feature y


## 1.4.1 - (2017-05-29)
---

### Changes
* updating documentation


...
```