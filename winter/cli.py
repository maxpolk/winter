'''
Command-line interface for Winter.

This file is part of Winter, a wiki-based computing platform.
Copyright (C) 2012,2014  Max Polk <maxpolk@gmail.com>
License located at http://www.gnu.org/licenses/agpl-3.0.html
'''

# Library imports
from optparse import OptionParser   # read/parse command-line options
import ConfigParser                 # read/write config file
import os

# Local imports
import winter
from winter.interwiki import Interwiki

# Module short description
module_description = "command-line interface"

# Module long description
long_description = "{} ({}): {}, {}".format (
    winter.software_name, winter.software_version,
    winter.software_description, module_description)

def setupOptions (args):
    '''
    Read and return parsed command-line options and arguments.
    Command-line options override config file options.
    '''
    # All options always exist because we use defaults if not present
    parser = OptionParser (prog=winter.software_name,
                           version=winter.software_version,
                           usage="Usage: %prog [options]",
                           description=long_description)

    # Verbose
    parser.add_option (
        "-v", "--verbose",
        dest = "verbose", action = "store_true", default = False,
        help = "display more information about client operation")

    # Config file
    parser.add_option (
        "-c", "--config",
        dest = "config", default = os.path.expanduser ("~/.winterrc"),
        metavar = "FILE",
        help = "configuration file [default: %default]")

    # No config, don't read or write config file, higher priority than -c option
    parser.add_option (
        "-n", "--noconfig",
        dest = "noconfig", action = "store_true", default = False,
        help = "do not use a configuration file")

    # Add a directory for local file wiki
    parser.add_option (
        "-d", "--directory",
        dest = "directory", default = os.path.expanduser ("~/.winter"),
        help = "add directory for local file wiki")

    # Add a MongoDB collection for database server wiki
    parser.add_option (
        "-m", "--mongo",
        dest = "collection", help = "add mongodb collection for database wiki")

    # Add an URL for web based wiki
    parser.add_option (
        "-u", "--url",
        dest = "url", help = "add url for web wiki")

    # Place results into temp variables
    (options, arguments) = parser.parse_args (args)

    if (options.verbose):
        def show (name, value):
            print "    {0:15}: {1}".format (name, value)
        # Debug temp variables
        print "Parsed command-line options: "
        show ("verbose", options.verbose)
        show ("config", options.config)
        show ("noconfig", options.noconfig)
        show ("collection", options.collection)
        show ("url", options.url)
        show ("directory", options.directory)
        if len(arguments) > 1:
            print "Parsed command-line arguments:"
            for arg in arguments[1:]:
                show ("argument", arg)

    return (parser.get_default_values(), options, arguments)

def setupSystem (default_options, options):
    '''
    Instantiate and return an interwiki system using the default and given options.
    '''
    # If not ignoring config file, read it
    if (not options.noconfig):
        # Read config file for config file options
        print "DEBUG: Reading configuration file (not yet)"
        pass

    # If not ignoring config file, write changes
    if (not options.noconfig):
        print "DEBUG: Writing configuration file (not yet)"
        pass

    # Create an interwiki agent
    interwiki = Interwiki ()
    return interwiki

def runCommands (interwiki, arguments):
    print "Running commands: (not yet)"
    for arg in arguments[1:]:
        print "    arg:", arg

# Running modules as top-level scripts is an antipattern
if __name__ == '__main__':
    pass
