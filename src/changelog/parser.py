from typing import Iterable, TypedDict, Optional, List, TypeVar

from changelog.utils import ChangelogUtils


class Changes(TypedDict):
    added: List[str]
    changed: List[str]
    deprecated: List[str]
    removed: List[str]
    fixed: List[str]
    security: List[str]


class Release(TypedDict):
    version: str
    date: Optional[str]
    sections: Changes


CL = ChangelogUtils()


def parse(data: Iterable[str]) -> Iterable[Release]:
    release = None
    section = None
    for current_line in data:
        if CL.match_version(current_line) or current_line.strip() == '## Unreleased':
            if release is not None:
                yield release
            if current_line == '## Unreleased':
                release = {'version': 'Unreleased', 'date': None, 'sections': {}}
            else:
                release = {'version': CL.match_version(current_line), 'date': '', 'sections': {}}
            section = None
        elif current_line.startswith('### '):
            section = current_line.replace('### ', '').strip().lower()
        elif release is not None and section is not None and current_line.strip() != "":
            release['sections'].setdefault(section, []).append(current_line.replace('*', '').strip())
    if release is not None:
        yield release

