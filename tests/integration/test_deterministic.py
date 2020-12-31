import os
import unittest
import random

from click.testing import CliRunner

from changelog.commands import cli
from changelog.utils import ChangelogUtils

START = random.getstate()

OPTIONS = [(section, "{}{{}}".format(section)) for section in ChangelogUtils.TYPES_OF_CHANGE]


class CliDeterministicTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        os.environ.setdefault('LC_ALL', 'en_US.utf-8')
        os.environ.setdefault('LANG', 'en_US.utf-8')
        random.setstate(START)

    def test_determinism(self):
        # first pass
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            self.runner.invoke(cli, ['added', "First Feature"])
            self.runner.invoke(cli, ['release', '--yes'])
            for i in range(random.randrange(10)):
                for j in range(random.randrange(3)):
                    line = random.choice(OPTIONS)
                    args = [line[0], line[1].format(random.random())]
                    self.runner.invoke(cli, args)
                self.runner.invoke(cli, ['release', '--yes'])
            with open("CHANGELOG.md", 'r') as first_pass_file:
                first_pass = first_pass_file.read()
        # reset random
        random.setstate(START)
        # second pass
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            self.runner.invoke(cli, ['added', "First Feature"])
            self.runner.invoke(cli, ['release', '--yes'])
            for i in range(random.randrange(10)):
                for j in range(random.randrange(3)):
                    line = random.choice(OPTIONS)
                    args = [line[0], line[1].format(random.random())]
                    self.runner.invoke(cli, args)
                self.runner.invoke(cli, ['release', '--yes'])
            with open("CHANGELOG.md", 'r') as second_pass_file:
                second_pass = second_pass_file.read()
        self.assertEqual(first_pass, second_pass)
