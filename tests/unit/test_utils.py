import unittest

from changelog.utils import bump_version, crunch_lines

class UtilsTestCase(unittest.TestCase):

    def test_bump_version_major(self):
        self.assertEqual(bump_version('0.1.0', 'major'), '1.0.0')

    def test_bump_version_minor(self):
        self.assertEqual(bump_version('0.1.0', 'minor'), '0.2.0')

    def test_bump_version_patch(self):
        self.assertEqual(bump_version('0.1.0', 'patch'), '0.1.1')

    def test_crunch_lines(self):
        document = [
            "this\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "that\n"
        ]
        self.assertEqual(crunch_lines(document), ['this\n', '\n', '\n', 'that\n'])

    def test_get_release_suggestion_patch(self):
        pass