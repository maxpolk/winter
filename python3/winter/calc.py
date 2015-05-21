# This file is part of Winter, a wiki-based computing platform.
# Copyright (C) 2012,2014,2015  Max Polk <maxpolk@gmail.com>
# License located at http://www.gnu.org/licenses/agpl-3.0.html
'''
Calc server that recalculates resources after they have been changed.
'''

# Requires version 3, say it now rather than fail mysteriously later
import sys
if (sys.version_info.major < 3):
    print ("Requires python 3")
    import os
    os._exit(1)

# Library imports
import pymongo

# Import the current package to get package vars like winter.software_name
import winter

# Module short description
module_description = "calc server module"

class CalcServer (object):
    '''
    The calc server of Winter.
    '''
    pass

# Running modules as top-level scripts is an antipattern, use bin/snow instead
if __name__ == '__main__':
    pass
