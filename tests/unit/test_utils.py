import unittest
import os
from datetime import date
from unittest.mock import patch

from changelog.utils import ChangelogUtils
from changelog.exceptions import ChangelogDoesNotExistError


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.cl = ChangelogUtils()

    def test_bump_version_major(self):
        self.assertEqual(self.cl.bump_version('0.1.0', 'major'), '1.0.0')

    def test_bump_version_minor(self):
        self.assertEqual(self.cl.bump_version('0.1.0', 'minor'), '0.2.0')

    def test_bump_version_patch(self):
        self.assertEqual(self.cl.bump_version('0.1.0', 'patch'), '0.1.1')

    def test_crunch_lines(self):
        document = [
            "this\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "that\n"
        ]
        self.assertEqual(self.cl.crunch_lines(document), ['this\n', '\n', '\n', 'that\n'])

    def test_crunch_lines_release(self):
        document = [
            "this\n",
            "---\n",
            "\n",
            "\n",
            "\n",
            "that\n"
        ]
        self.assertEqual(self.cl.crunch_lines(document), ['this\n', '---\n', '\n', 'that\n'])

    def test_get_release_suggestion_patch(self):
        with patch.object(ChangelogUtils, 'get_unreleased_change_types', return_value={'changed': ''}):
            CL = ChangelogUtils()
            result = CL.get_release_suggestion()
            self.assertEqual(result, 'patch')

    def test_get_release_suggestion_minor(self):
        with patch.object(ChangelogUtils, 'get_unreleased_change_types', return_value={'added': 'stuff'}):
            CL = ChangelogUtils()
            result = CL.get_release_suggestion()
            self.assertEqual(result, 'minor')

    def test_get_release_suggestion_major(self):
        with patch.object(ChangelogUtils, 'get_unreleased_change_types', return_value={'removed': 'stuff'}):
            CL = ChangelogUtils()
            result = CL.get_release_suggestion()
            self.assertEqual(result, 'major')

    def test_get_release_suggestion_minor_with_beta_headers(self):
        with patch.object(ChangelogUtils, 'get_unreleased_change_types', return_value={'new': 'stuff'}):
            CL = ChangelogUtils()
            result = CL.get_release_suggestion()
            self.assertEqual(result, 'minor')

    def test_get_release_suggestion_major_with_beta_headers(self):
        with patch.object(ChangelogUtils, 'get_unreleased_change_types', return_value={'breaks': 'stuff'}):
            CL = ChangelogUtils()
            result = CL.get_release_suggestion()
            self.assertEqual(result, 'major')

    def test_update_section(self):
        with patch.object(ChangelogUtils, 'write_changelog') as mock_write:
            sample_data = [
                "## Unreleased\n",
                "---\n",
                "\n",
                "### Added\n",
                "\n",
                "### Fixed\n",
                "\n",
                "### Removed\n",
            ]
            with patch.object(ChangelogUtils, 'get_changelog_data', return_value=sample_data) as mock_read:
                CL = ChangelogUtils()
                CL.update_section("added", 'this is a test')
        mock_write.assert_called_once_with([
            "## Unreleased\n",
            "---\n",
            "\n",
            "### Added\n",
            "* this is a test\n",
            "\n",
            "### Fixed\n",
            "\n",
            "### Removed\n",
        ])

    def test_get_current_version(self):
        sample_data = [
            "## Unreleased\n",
            "---\n",
            "\n",
            "### Added\n",
            "\n",
            "### Fixed\n",
            "\n",
            "### Removed\n",
            "\n",
            "\n",
            "## [0.3.2] - (2017-06-09)\n",
            "---\n",
        ]
        with patch.object(ChangelogUtils, 'get_changelog_data', return_value=sample_data) as mock_read:
            CL = ChangelogUtils()
            result = CL.get_current_version()
        self.assertEqual(result, '0.3.2')

    def test_get_current_version_default(self):
        sample_data = []
        with patch.object(ChangelogUtils, 'get_changelog_data', return_value=sample_data) as mock_read:
            CL = ChangelogUtils()
            result = CL.get_current_version()
        self.assertEqual(result, '0.0.0')

    def test_get_changes(self):
        sample_data = [
            "## Unreleased\n",
            "---\n",
            "\n",
            "### Added\n",
            "* added feature x\n",
            "\n",
            "### Fixed\n",
            "* fixed bug 1\n",
            "\n",
            "### Removed\n",
            "\n",
            "\n",
            "## 0.3.2 - (2017-06-09)\n",
            "---\n",
        ]
        with patch.object(ChangelogUtils, 'get_changelog_data', return_value=sample_data) as mock_read:
            CL = ChangelogUtils()
            result = CL.get_unreleased_change_types()
        self.assertTrue('added' in result)
        self.assertTrue('fixed' in result)

    def test_get_changes_works_with_beta_headers(self):
        sample_data = [
            "## Unreleased\n",
            "---\n",
            "\n",
            "### New\n",
            "* added feature x\n",
            "\n",
            "### Changes\n",
            "* changes feature x\n",
            "\n",
            "### Fixes\n",
            "* fixed bug 1\n",
            "\n",
            "### Breaks\n",
            "\n",
            "\n",
            "## 0.3.2 - (2017-06-09)\n",
            "---\n",
        ]
        with patch.object(ChangelogUtils, 'get_changelog_data', return_value=sample_data) as mock_read:
            CL = ChangelogUtils()
            result = CL.get_unreleased_change_types()
        self.assertTrue('new' in result)
        self.assertTrue('changes' in result)
        self.assertTrue('fixes' in result)

    def test_get_new_release_version_patch(self):
        with patch.object(ChangelogUtils, 'get_current_version', return_value='1.1.1'):
            CL = ChangelogUtils()
            self.assertEqual(CL.get_new_release_version('patch'), '1.1.2')

    def test_get_new_release_version_minor(self):
        with patch.object(ChangelogUtils, 'get_current_version', return_value='1.1.1'):
            CL = ChangelogUtils()
            self.assertEqual(CL.get_new_release_version('minor'), '1.2.0')

    def test_get_new_release_version_major(self):
        with patch.object(ChangelogUtils, 'get_current_version', return_value='1.1.1'):
            CL = ChangelogUtils()
            self.assertEqual(CL.get_new_release_version('major'), '2.0.0')

    def test_get_new_release_version_suggest(self):
        with patch.object(ChangelogUtils, 'get_current_version', return_value='1.1.1'):
            with patch.object(ChangelogUtils, 'get_release_suggestion', return_value='minor'):
                CL = ChangelogUtils()
                self.assertEqual(CL.get_new_release_version('suggest'), '1.2.0')


class ChangelogFileOperationTestCase(unittest.TestCase):
    def setUp(self):
        self.CL = ChangelogUtils()
        self.CL.CHANGELOG = 'TEST_CHANGELOG.md'

    def test_initialize_changelog_file(self):
        self.CL.initialize_changelog_file()
        self.assertTrue(os.path.isfile('TEST_CHANGELOG.md'))

    def test_initialize_changelog_file_exists(self):
        self.CL.initialize_changelog_file()
        self.assertTrue(os.path.isfile('TEST_CHANGELOG.md'))
        message = self.CL.initialize_changelog_file()
        self.assertEqual(message, 'TEST_CHANGELOG.md already exists')

    def test_get_changelog_data(self):
        self.CL.initialize_changelog_file()
        data = self.CL.get_changelog_data()
        self.assertTrue(len(data) > 1)

    def test_get_changelog_no_file(self):
        self.assertRaises(ChangelogDoesNotExistError, self.CL.get_changelog_data)

    def test_write_changelog(self):
        self.CL.initialize_changelog_file()
        original = self.CL.get_changelog_data()
        data = original + ["test\n"]
        self.CL.write_changelog(data)
        modified = self.CL.get_changelog_data()
        self.assertEqual(len(original) + 1, len(modified))

    def test_cut_release(self):
        self.CL.initialize_changelog_file()
        self.CL.update_section('added', "this is a test")
        self.CL.cut_release('suggest')
        data = self.CL.get_changelog_data()
        self.assertTrue('## Unreleased\n' in data)
        self.assertTrue(f'## [0.1.0] - ({date.today().isoformat()})\n' in data)
        self.CL.update_section('removed', "removed a thing")
        self.CL.cut_release('suggest')
        data2 = self.CL.get_changelog_data()
        self.assertTrue('## Unreleased\n' in data2)

    def test_cut_release_works_with_beta_headers(self):
        sample_data = [
            "## Unreleased\n",
            "---\n",
            "\n",
            "### New\n",
            "* added feature x\n",
            "\n",
            "### Changes\n",
            "* changes feature x\n",
            "\n",
            "### Fixes\n",
            "* fixed bug 1\n",
            "\n",
            "### Breaks\n",
            "\n",
            "\n",
            "## [0.3.2] - (2017-06-09)\n",
            "---\n",
        ]
        with patch.object(ChangelogUtils, 'get_changelog_data', return_value=sample_data) as mock_read:
            CL = ChangelogUtils()
            CL.cut_release('suggest')
        data = CL.get_changelog_data()
        self.assertTrue('## Unreleased\n' in data)
        self.assertTrue(f'## [0.4.0] - ({date.today().isoformat()})\n' in data)
        # The beta headings still exist
        self.assertTrue('### New\n' in data)
        self.assertTrue('### Changes\n' in data)
        self.assertTrue('### Fixes\n' in data)
        # The new headings exist
        self.assertTrue('### Added\n' in data)
        self.assertTrue('### Changed\n' in data)
        self.assertTrue('### Deprecated\n' in data)
        self.assertTrue('### Removed\n' in data)
        self.assertTrue('### Fixed\n' in data)
        self.assertTrue('### Security\n' in data)

    def test_match_version_canonical(self):
        line = "## [0.2.1] - (2017-06-09)"
        self.assertEqual(self.CL.match_version(line), '0.2.1')

    def test_match_version_miss(self):
        line = '### Changed'
        self.assertFalse(self.CL.match_version(line))

    def test_match_version_basic(self):
        line = '## [v4.1.3]'
        self.assertEqual(self.CL.match_version(line), '4.1.3')

    def test_match_keep_a_changelog(self):
        line = '## [4.1.3] - 2017-06-20'
        self.assertEqual(self.CL.match_version(line), '4.1.3')

    def tearDown(self):
        try:
            os.remove('TEST_CHANGELOG.md')
        except Exception:
            pass
