import unittest
from click.testing import CliRunner

class CliIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_integration(self):
        pass
