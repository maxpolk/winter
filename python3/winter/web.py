# This file is part of Winter, a wiki-based computing platform.
# Copyright (C) 2012,2014,2015  Max Polk <maxpolk@gmail.com>
# License located at http://www.gnu.org/licenses/agpl-3.0.html
'''
Web server that provides the web interface to Winter.
'''

# Requires version 3, say it now rather than fail mysteriously later.
# Won't work if you use Python 3 exclusive syntax anywhere in the file.
import sys
if (sys.version_info.major < 3):
    exit ("Requires python 3")

# Library imports
import pymongo

# Import the current package to get package vars like winter.software_name
import winter

# Module short description
module_description = "web server module"

class WebServer (object):
    '''
    The web server of Winter.
    '''
    pass

# Running modules as top-level scripts is an antipattern, use bin/snow instead
if __name__ == '__main__':
    pass
