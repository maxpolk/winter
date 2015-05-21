'''
Script to run tests.

This file is part of Winter, a wiki-based computing platform.
Copyright (C) 2012,2014,2015  Max Polk <maxpolk@gmail.com>
License located at http://www.gnu.org/licenses/agpl-3.0.html
'''

# Requires version 3, say it now rather than fail mysteriously later
import sys
if (sys.version_info.major < 3):
    print ("Requires python 3")
    import os
    os._exit(1)

import unittest

from winter import initiate, notify, calc, web

class TestMetadata (unittest.TestCase):
    def test_description (self):
        assert len (initiate.module_description) > 0, 'initiate: invalid module_description'
        assert len (notify.module_description) > 0, 'nofity: invalid module_description'
        assert len (calc.module_description) > 0, 'calc: invalid module_description'
        assert len (web.module_description) > 0, 'web: invalid module_description'

if __name__ == '__main__':
    unittest.main ()
