import os
import re
from datetime import date
from typing import cast, Dict, List, Optional, Set

from changelog.templates import BASE, RELEASE_LINE, DEFAULT_VERSION, RELEASE_LINE_REGEXES
from changelog.exceptions import ChangelogDoesNotExistError

Lines = List[str]

class ChangelogUtils:
    CHANGELOG: str = 'CHANGELOG.md'
    TYPES_OF_CHANGE: List[str] = ['added', 'changed', 'deprecated', 'removed', 'fixed', 'security']
    SECTIONS: Dict[str, str] = {change_type: f"### {change_type.capitalize()}\n" for change_type in TYPES_OF_CHANGE}
    REVERSE_SECTIONS: Dict[str, str] = {v: k for k, v in SECTIONS.items()}

    # These were the sections before v1.0.0
    # Kept so that user from pre-v1.0.0 versions can upgrade
    BETA_TYPES_OF_CHANGE: List[str] = ['new', 'changes', 'fixes', 'breaks']
    BETA_SECTIONS: Dict[str, str] = {change_type: f"### {change_type.capitalize()}\n" for change_type in BETA_TYPES_OF_CHANGE}
    BETA_REVERSE_SECTIONS: Dict[str, str] = {v: k for k, v in BETA_SECTIONS.items()}

    UNRELEASED: str = "\n## Unreleased\n---\n\n" + ''.join([f"{section_header}\n\n" for section_header in REVERSE_SECTIONS.keys()])
    INIT: str = BASE + UNRELEASED
    VERSION_FORMAT: str = "date"

    def initialize_changelog_file(self) -> str:
        """
        Creates a changelog if one does not already exist
        """
        if os.path.isfile(self.CHANGELOG):
            return f"{self.CHANGELOG} already exists"
        with open(self.CHANGELOG, 'w') as changelog:
            changelog.write(self.INIT)
        return f"Created {self.CHANGELOG}"

    def get_changelog_data(self) -> Lines:
        """
        Gets all of the lines from the current changelog
        """
        if not os.path.isfile(self.CHANGELOG):
            raise ChangelogDoesNotExistError
        with open(self.CHANGELOG, 'r') as changelog:
            data = changelog.readlines()
        return data

    def write_changelog(self, line_list: Lines) -> None:
        """
        writes the lines out to the changelog
        """
        with open(self.CHANGELOG, 'w') as changelog:
            changelog.writelines(line_list)

    def update_section(self, section, message: str) -> None:
        """Updates a section of the changelog with message"""
        data = self.get_changelog_data()
        i = data.index(self.SECTIONS[section]) + 1
        data.insert(i, f"* {message}\n")
        self.write_changelog(data)

    def get_current_version(self) -> str:
        """Gets the Current Application Version Based on Changelog"""
        data = self.get_changelog_data()
        for line in data:
            match = self.match_version(line)
            if match:
                return match
        return DEFAULT_VERSION

    def get_unreleased_change_types(self) -> Set[str]:
        """Get the list of chances since the last release"""
        data = self.get_changelog_data()
        change_types = set()
        reading = False
        section = None
        for line in data:
            if line in ['---\n', '\n']:
                continue
            if self.match_version(line):
                break
            if reading:
                if line in self.REVERSE_SECTIONS:
                    section = self.REVERSE_SECTIONS[line]
                    continue
                if line in self.BETA_REVERSE_SECTIONS:
                    section = self.BETA_REVERSE_SECTIONS[line]
                    continue
                change_types.add(cast(str, section))
                continue
            if line == "## Unreleased\n":
                reading = True
                continue

        return change_types

    def get_release_suggestion(self) -> str:
        """Suggests a release type"""
        change_types = self.get_unreleased_change_types()
        if 'removed' in change_types or 'breaks' in change_types:
            return "major"
        if 'added' in change_types or 'new' in change_types:
            return "minor"
        return "patch"

    def get_new_release_version(self, release_type: str) -> str:
        """
        Returns the version of the new release
        """
        current_version = self.get_current_version()
        if release_type not in ['major', 'minor', 'patch']:
            release_type = self.get_release_suggestion()
        return self.bump_version(current_version, release_type)

    def cut_release(self, release_type: str = "suggest") -> None:
        """Cuts a release and updates changelog"""
        new_version = self.get_new_release_version(release_type)
        change_types = self.get_unreleased_change_types()
        data = self.get_changelog_data()
        output = []
        unreleased_position = 0
        reading = True
        for i, line in enumerate(data):
            if self.match_version(line):
                reading = False
            if line == "## Unreleased\n":
                unreleased_position = i
                line = RELEASE_LINE[self.VERSION_FORMAT].format(new_version, date.today().isoformat())
            if reading and line in self.REVERSE_SECTIONS and self.REVERSE_SECTIONS[line] not in change_types:
                continue
            output.append(line)
        output.insert(unreleased_position, self.UNRELEASED)
        output = self.crunch_lines(output)
        self.write_changelog(output)

    def crunch_lines(self, line_list: Lines) -> Lines:
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
            elif minus_2 == '---\n' and here == minus_1 == '\n':
                line_list.pop(i)
            else:
                i += 1
        return line_list

    def bump_version(self, version: str, release_type: str) -> str:
        """
        Bumps a version number based on release_type
        """
        x, y, z = [int(i) for i in version.split(".")]
        if release_type == "major":
            x += 1
            y = z = 0
        elif release_type == "minor":
            y += 1
            z = 0
        else:
            z += 1
        return f"{x}.{y}.{z}"

    def match_version(self, line: str) -> Optional[str]:
        """
        Matches a line vs the list of version strings. Returns group, or None if no match is found.
        """
        for version_format, regex in RELEASE_LINE_REGEXES.items():
            match = re.match(regex, line)
            if match and match.group('v'):
                self.VERSION_FORMAT = version_format
                return match.group('v')
        return None
