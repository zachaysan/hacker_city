import unittest
from crawlers.github import Github

class Test_Github(unittest.TestCase):
    def test_init(self):
        g = Github()
        self.assertTrue(g)
