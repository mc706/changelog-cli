# Changelog CLI
[![PyPI version](https://badge.fury.io/py/changelog-cli.svg)](https://badge.fury.io/py/changelog-cli)
[![Build Status](https://travis-ci.org/mc706/changelog-cli.svg?branch=master)](https://travis-ci.org/mc706/changelog-cli)
[![Code Health](https://landscape.io/github/mc706/changelog-cli/master/landscape.svg?style=flat)](https://landscape.io/github/mc706/changelog-cli/master)
[![Coverage Status](https://coveralls.io/repos/github/mc706/changelog-cli/badge.svg?branch=master)](https://coveralls.io/github/mc706/changelog-cli?branch=master)

A command line interface for managing your CHANGELOG.md files.

## Commands
`changelog init` -> Creates a CHANGELOG.md

`changelog (new|change|fix|break) <message>` -> adds a line to the appropriate section

`changelog release --major|minor|patch|suggest)` -> Cuts a release for the changelog, incrementing the version

