'''
Server module for Winter.

This file is part of Winter, a wiki-based computing platform.
Copyright (C) 2012,2014  Max Polk <maxpolk@gmail.com>
License located at http://www.gnu.org/licenses/agpl-3.0.html
'''

# Library imports
import argparse                     # read/parse command-line options
import ConfigParser                 # read/write config file
import os

# Import the current package to get package vars like winter.software_name
import winter

# Module short description
module_description = "server module"

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
    parser = argparse.ArgumentParser (prog=winter.software_name,
                                      usage="Usage: %prog [options]",
                                      description=long_description)

    # Version
    parser.add_argument (
        "--version",
        action="version", version=winter.software_version)

    # Verbose
    parser.add_argument (
        "-v", "--verbose",
        action = "store_true", default = False,
        help = "display more information about client operation")

    # Config file for various options
    parser.add_argument (
        "-c", "--config",
        default = os.path.expanduser ("~/.winterrc"),
        metavar = "FILE",
        help = "configuration file [default: %default]")

    # No config, don't read or write config file, higher priority than -c option
    parser.add_argument (
        "-n", "--noconfig",
        action = "store_true", default = False,
        help = "do not use a configuration file")

    # Directory to be used for file cache, overrides config file value
    parser.add_argument (
        "-d", "--directory",
        default = os.path.expanduser ("~/.winter"),
        help = "directory to be used for file cache")

    # Add hostname where to find MongoDB database
    parser.add_argument (
        "--dbhost",
        default = '127.0.0.1',
        help = "hostname of MongoDB database")

    # Add a port number to MongoDB database
    parser.add_argument (
        "--dbport",
        default = 27017,
        type = int,
        help = "port number of MongoDB database")

    # Everything else goes into "arguments" option
    parser.add_argument (
        "arguments",
        nargs = argparse.REMAINDER)

    # Place results into options variable
    options = parser.parse_args (args)

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
        if len(options.arguments) > 1:
            print "Parsed command-line arguments:"
            for arg in options.arguments[1:]:
                show ("argument", arg)

    return options

def setupSystem (options):
    '''
    Instantiate and return an wiki system using the default and given options.
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

    return "TODO"

def runCommands (wiki):
    print "Running commands: (not yet)"
    # for arg in arguments[1:]:
    #     print "    arg:", arg

# Running modules as top-level scripts is an antipattern, use bin/snow instead
if __name__ == '__main__':
    pass
