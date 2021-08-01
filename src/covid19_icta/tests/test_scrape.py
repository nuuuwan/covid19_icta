import unittest

from covid19_icta import scrape


class TestCase(unittest.TestCase):
    def test_dump(self):
        self.assertTrue(scrape._run())


if __name__ == '__main__':
    unittest.main()
