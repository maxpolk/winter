'''
Server module for Winter.

This file is part of Winter, a wiki-based computing platform.
Copyright (C) 2012,2014  Max Polk <maxpolk@gmail.com>
License located at http://www.gnu.org/licenses/agpl-3.0.html
'''

# Library imports
import argparse                         # read/parse command-line options
import os

try:
    from configparser import ConfigParser # Python 3 configuration file parsing
except:
    from ConfigParser import ConfigParser # Python 2 configuration file parsing

# Import the current package to get package vars like winter.software_name
import winter

# Module short description
module_description = "server module"

# Module long description
long_description = "{} ({}): {}".format (
    winter.software_name, winter.software_version, winter.software_description)

def setupOptions (args):
    '''
    Read and return parsed command-line options and arguments.
    Command-line options override config file options.
    '''
    # All options always exist because we use defaults if not present
    parser = argparse.ArgumentParser (prog=winter.software_name,
                                      usage="%(prog)s [options] [arguments]",
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

    # No config, don't read or write config file, higher priority than -c option
    parser.add_argument (
        "-n", "--noconfig",
        action = "store_true", default = False,
        help = "do not use a configuration file")

    # Config file for various options
    parser.add_argument (
        "-c", "--config",
        default = os.path.expanduser ("~/.winterrc"),
        metavar = "FILE",
        help = "configuration file  [default: %(default)s]")

    # What profile within the config file to use
    parser.add_argument (
        "-p", "--profile",
        default = "DEFAULT",            # has magic properties in ConfigParser
        help = "configuration file profile to use")

    # Save configuration file with current options under given profile name
    parser.add_argument (
        "-s", "--save",
        action = "store_true", default = False,
        help = "save configuration file under given profile name")

    # Directory to be used for file cache, overrides config file value
    parser.add_argument (
        "-d", "--directory",
        default = os.path.expanduser ("~/.winter"),
        help = "directory to be used for file cache [default: %(default)s]")

    # Add hostname where to find MongoDB database
    parser.add_argument (
        "--dbhost",
        default = '127.0.0.1',
        help = "hostname of MongoDB database [default: %(default)s]")

    # Add a port number to MongoDB database
    parser.add_argument (
        "--dbport",
        default = 27017,
        type = int,
        help = "port number of MongoDB database [default: %(default)s]")

    # Add database name to use for MongoDB database
    parser.add_argument (
        "--dbname",
        default = 'winter',
        help = "database name to use inside MongoDB database [default: %(default)s]")

    # Everything else goes into "arguments" option
    parser.add_argument (
        "arguments",
        nargs = argparse.REMAINDER)

    # Place results into options variable
    options = parser.parse_args (args)

    # If verbose, dump config options gathered
    if (options.verbose):
        def show (name, value, default_value):
            suffix = ""
            if (default_value is not None and value != default_value):
                suffix = " (default {})".format (default_value)
            print "    {0:15}: {1}{2}".format (name, value, suffix)
        # Turn options into a dictionary and iterate
        print "Parsed command-line options: "
        option_dict = vars (options)
        for key in sorted (option_dict):
            # Get default value for option
            default_value = parser.get_default (key)
            value = getattr (options, key) # option_dict[key]
            is_default = (default_value == value)
            show (key, value, default_value)
        if len(options.arguments) > 1:
            print "Parsed command-line arguments:"
            for arg in options.arguments:
                show ("argument", arg, None)

    # Optionally read configuration file
    if (not options.noconfig):
        # options.verbose (verbosity)
        # options.noconfig (overrides config)
        # options.config (filename)
        # options.profile (profile name within config file)
        # options.save (save config file)
        # options.directory (cache dir)
        # options.dbhost (database host)
        # options.dbport (database port)
        # options.dbname (database name)
        # options.arguments  (everything else)
        if (options.verbose):
            print ("Reading config file {}".format (options.config))
        config = ConfigParser ()
        config.read (options.config)
        if (options.save):
            # Save config file
            print "Writing configuration file (not yet)"

    #
    # config: get, getint, getfloat(), getboolean()
    #
    # import configparser
    # config = configparser.ConfigParser()
    #
    # WRITING
    #
    # config['DEFAULT'] = {'ServerAliveInterval': '45',
    # ...                  'Compression': 'yes',
    # ...                  'CompressionLevel': '9'}
    # config['bitbucket.org'] = {}
    # config['bitbucket.org']['User'] = 'hg'
    # config['topsecret.server.com'] = {}
    # topsecret = config['topsecret.server.com']
    # topsecret['Port'] = '50022'     # mutates the parser
    # topsecret['ForwardX11'] = 'no'  # same here
    # config['DEFAULT']['ForwardX11'] = 'yes'
    # with open('example.ini', 'w') as configfile:
    # ...   config.write(configfile)
    #
    # READING
    #
    # config.read('example.ini')    # ['example.ini']
    # config.sections()             # ['bitbucket.org', 'topsecret.server.com']
    # 'bitbucket.org' in config     # True
    # 'bytebong.com' in config      # False
    # config['bitbucket.org']['User']    # some string
    # config['DEFAULT']['Compression']   # some string
    # topsecret = config['topsecret.server.com']
    # topsecret['ForwardX11']       # section value
    # topsecret['Port']             # '50022' not an int, use getint instead
    # for key in config['bitbucket.org'] ....
    #
    return options

def setupSystem (options):
    '''
    Instantiate and return an wiki system using the default and given options.
    '''
    return "TODO"

def runCommands (wiki):
    print "Running commands: (not yet)"
    # for arg in arguments[1:]:
    #     print "    arg:", arg

# Running modules as top-level scripts is an antipattern, use bin/snow instead
if __name__ == '__main__':
    pass
