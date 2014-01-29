# -*- coding: utf-8 -*-
import os
import sys
import unittest

dir_test = os.path.dirname(os.path.abspath(__file__))
dir_root = os.path.dirname(dir_test)
sys.path.insert(0, dir_root)

from threaddit.bot import extract_urls


class ThreadditUrlsTestSuite(unittest.TestCase):
    """URLs test cases."""

    def test_extract_urls(self):
        with open(dir_test + '/urls.md', 'r') as f:
            md = f.read()
        urls = extract_urls(md)
        self.assertEqual(3, len(urls))


if __name__ == '__main__':
    unittest.main()
