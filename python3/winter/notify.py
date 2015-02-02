# This file is part of Winter, a wiki-based computing platform.
# Copyright (C) 2012,2014,2015  Max Polk <maxpolk@gmail.com>
# License located at http://www.gnu.org/licenses/agpl-3.0.html
'''
WebSocket server for notifications about calculated resources.
'''

# Library imports
import pymongo

# Import the current package to get package vars like winter.software_name
import winter

# Module short description
module_description = "notify server module"

class NotifyServer (object):
    '''
    The notification server of Winter.
    '''
    pass

# Running modules as top-level scripts is an antipattern, use bin/snow instead
if __name__ == '__main__':
    pass
