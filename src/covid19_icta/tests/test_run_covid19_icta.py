import unittest

from covid19_icta import run_covid19_icta


class TestCase(unittest.TestCase):

    def test_dump(self):
        self.assertTrue(run_covid19_icta._run())


if __name__ == '__main__':
    unittest.main()
