'''
Script to run tests.

This file is part of Winter, a wiki-based computing platform.
Copyright (C) 2012,2014  Max Polk <maxpolk@gmail.com>
License located at http://www.gnu.org/licenses/agpl-3.0.html
'''

import unittest

import winter.server

class TestMetadata (unittest.TestCase):
    def test_description (self):
        assert len (winter.server.module_description) > 0, 'invalid module_description'

if __name__ == '__main__':
    unittest.main ()
