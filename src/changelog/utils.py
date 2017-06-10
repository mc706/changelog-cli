import os
import re
from datetime import date

from changelog.templates import INIT, UNRELEASED, RELEASE_LINE, RELEASE_LINE_REGEX, DEFAULT_VERSION
from changelog.exceptions import ChangelogDoesNotExistError

CHANGELOG = 'CHANGELOG.md'
SECTIONS = {
    'new': "### New\n",
    'fix': "### Fixes\n",
    'change': '### Changes\n',
    'break': "### Breaks\n"
}
REVERSE_SECTIONS = {v: k for k, v in SECTIONS.items()}


def initialize_changelog_file():
    """
    Creates a changelog if one does not already exist
    """
    if os.path.isfile(CHANGELOG):
        return "CHANGELOG.md already exists"
    with open("CHANGELOG.md", 'w') as changelog:
        changelog.write(INIT)
    return "Created CHANGELOG.md"


def get_changelog_data():
    """
    Gets all of the lines from the current changelog
    """
    if not os.path.isfile(CHANGELOG):
        raise ChangelogDoesNotExistError
    with open(CHANGELOG, 'r') as changelog:
        data = changelog.readlines()
    return data


def write_changelog(line_list):
    """
    writes the lines out to the changelog
    """
    with open(CHANGELOG, 'w') as changelog:
        changelog.writelines(line_list)


def update_section(section, message):
    """Updates a section of the changelog with message"""
    data = get_changelog_data()
    i = data.index(SECTIONS[section]) + 1
    data.insert(i, "* {}\n".format(message))
    write_changelog(data)


def get_current_version():
    """Gets the Current Application Version Based on Changelog"""
    data = get_changelog_data()
    for line in data:
        match = re.match(RELEASE_LINE_REGEX, line)
        if match:
            return match.groups()[0]
    return DEFAULT_VERSION


def get_changes():
    """Get the list of chances since the last release"""
    data = get_changelog_data()
    changes = {}
    reading = False
    section = None
    for line in data:
        if line in ['---\n', '\n']:
            continue
        if re.match(RELEASE_LINE_REGEX, line):
            break
        if reading:
            if line in REVERSE_SECTIONS:
                section = REVERSE_SECTIONS[line]
                continue
            else:
                changes[section] = line.strip().lstrip("* ")
                continue
        if line == "## Unreleased\n":
            reading = True
            continue

    return changes


def get_release_suggestion():
    """Suggests a release type"""
    changes = get_changes()
    if 'break' in changes:
        return "major"
    elif 'new' in changes:
        return "minor"
    return "patch"


def get_new_release_version(release_type):
    """
    Returns the version of the new release
    """
    current_version = get_current_version()
    if release_type not in ['major', 'minor', 'patch']:
        release_type = get_release_suggestion()
    return bump_version(current_version, release_type)


def cut_release(release_type="suggest"):
    """Cuts a release and updates changelog"""
    new_version = get_new_release_version(release_type)
    changes = get_changes()
    data = get_changelog_data()
    output = []
    reading = True
    for line in data:
        if re.match(RELEASE_LINE_REGEX, line):
            reading = False
        if line == "## Unreleased\n":
            line = RELEASE_LINE.format(new_version, date.today().isoformat())
        if reading and line in REVERSE_SECTIONS and REVERSE_SECTIONS[line] not in changes:
            continue
        output.append(line)
    output.insert(5, UNRELEASED)
    output = crunch_lines(output)
    write_changelog(output)


def crunch_lines(line_list):
    """
    Removes triplicate blank lines from changelog to prevent it from getting too long
    """
    i = 2
    while i < len(line_list):
        here = line_list[i]
        minus_1 = line_list[i - 1]
        minus_2 = line_list[i - 2]
        if here == minus_1 == minus_2 == "\n":
            line_list.pop(i)
        else:
            i += 1
    return line_list


def bump_version(version, release_type):
    """
    Bumps a version number based on release_type
    """
    x, y, z = version.split(".")
    if release_type == "major":
        x = int(x) + 1
        y = z = 0
    elif release_type == "minor":
        y = int(y) + 1
        z = 0
    else:
        z = int(z) + 1
    return "{}.{}.{}".format(x, y, z)
