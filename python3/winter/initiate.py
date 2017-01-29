# This file is part of Winter, a wiki-based computing platform.
# Copyright (C) 2012,2014,2015  Max Polk <maxpolk@gmail.com>
# License located at http://www.gnu.org/licenses/agpl-3.0.html
'''
Server that launches notification (notify), web, and calculation (calc) servers.

Create the Setup class with command-line arguments, then ask it to createSystem
to create a System object upon which you can runCommands.

All service control occurs here, starting, stopping, and monitoring needed
servers.
'''

# Requires version 3, say it now rather than fail mysteriously later
import sys
if (sys.version_info.major < 3):
    exit ("Requires python 3")

# Library imports
import argparse                         # read/parse command-line options
import os
import pymongo
import multiprocessing

from configparser import ConfigParser

# Import the current package to get package vars like winter.software_name
import winter

# Module short description
module_description = "initiate server module"

class Setup (object):
    '''
    The constructor sets up all options and commands from the command-line and
    config file, then optionally writes your options to a config file to simply
    startup next time.  The createSystem method returns a System object you can
    call runCommands on to run the commands you setup.

    Example to skip configuration file, provide alternate db host, execute "run" command:

    >>>> setup = Setup (["--noconfig", "--dbhost", "192.168.1.103", "run"])
    >>>> setup.createSystem ().runCommands ()

    Example writing to default config file ~/.winterrc an alternative profile called
    "dbtest" with the command to "test_db_connection", then exiting.

    >>>> Setup (["--profile", "dbtest", "--dbhost", "192.168.1.103", "--save"])

    Example to start and run the system using the "dbtest" profile you previously setup:

    >>>> setup = Setup (["--profile", "dbtest", "run"])
    >>>> setup.createSystem ()
    >>>> system.runCommands ()

    Example to change default database server and port to simplify running next time:

    >>>> Setup (["--dbhost", "192.168.1.103", "--dbport", "33456", "--save"])

    Example to start and run system using defaults you established:

    >>>> setup = Setup (["run"])
    >>>> setup.createSystem ().runCommands ()
    '''

    # This is always loaded first, so global init methods go here.
    # Setting start method causes child python interpreters to not inherit from parent.
    multiprocessing.set_start_method ("spawn")

    # Create a long description from the package init vars
    long_description = "{} ({}): {}".format (
        winter.software_name, winter.software_version, winter.software_description)

    def __init__ (self, args):
        '''
        Read and return parsed command-line options and command arguments.  Command-line
        options override config file options; but defaults don't override.  Can't use
        defaults for parser because it doesn't help us know whether a value of default
        occurred because the user let it default by omitting it (which we want to
        override with config file) versus the user specifying the default explicitly
        (which we want to honor).
        '''
        # Manually establish application defaults here
        defaults = {
            "directory": os.path.expanduser ("~/.winter"),
            "dbhost": '127.0.0.1',
            "dbport": 27017,
            "dbname": 'winter',
            "dbuser": None,
            "dbpassword": None
        }

        # All options always exist because we use defaults if not present
        parser = argparse.ArgumentParser (prog=winter.software_name,
                                          usage="%(prog)s [options] [commands]",
                                          description=self.long_description)

        # Version: display and exit
        parser.add_argument (
            "--version",
            action="version", version=winter.software_version)

        # Verbose: increase verbosity of command-line print output
        parser.add_argument (
            "-v", "--verbose",
            action = "store_true", default = False,
            help = "display more information about client operation")

        # No config: don't read or write config file, higher priority than -c option
        parser.add_argument (
            "-n", "--noconfig",
            action = "store_true", default = False,
            help = "do not use a configuration file")

        # Config: specify file for various options
        parser.add_argument (
            "-c", "--config",
            default = os.path.expanduser ("~/.winterrc"),
            metavar = "FILE",
            help = "configuration file  [default: %(default)s]")

        # Profile: specify which profile within the config file to use
        parser.add_argument (
            "-p", "--profile",
            default = "DEFAULT",            # has magic properties in ConfigParser
            help = "configuration file profile to use")

        # Save: save configuration file with current options under given profile name
        parser.add_argument (
            "-s", "--save",
            action = "store_true", default = False,
            help = "save configuration file under given profile name")

        # Directory: dir to be used for file cache, overrides config file value
        parser.add_argument (
            "-d", "--directory",
            default = argparse.SUPPRESS,
            help = "directory to be used for file cache [default: {}]".format (
                defaults['directory']))

        # DB host: specify hostname where to find MongoDB database
        parser.add_argument (
            "--dbhost",
            default = argparse.SUPPRESS,
            help = "hostname of MongoDB database [default: {}]".format (
                defaults['dbhost']))

        # DB port: specify port number to MongoDB database
        parser.add_argument (
            "--dbport",
            default = argparse.SUPPRESS,
            type = int,
            help = "port number of MongoDB database [default: {}]".format (
                defaults['dbport']))

        # DB name: specify database name to use for MongoDB database
        parser.add_argument (
            "--dbname",
            default = argparse.SUPPRESS,
            help = "database name to use inside MongoDB database [default: {}]".format (
                defaults['dbname']))

        # DB user: specify user to authenticate to MongoDB database
        parser.add_argument (
            "--dbuser",
            default = argparse.SUPPRESS,
            help = "database user to authenticate as to MongoDB")

        # DB password: specify password to authenticate to MongoDB database
        parser.add_argument (
            "--dbpassword",
            default = argparse.SUPPRESS,
            help = "database password to use when authenticating to MongoDB")

        # Everything else goes into "commands".
        #
        # We fill choices with methods of System tagged with @command, which
        # are the only valid command methods in the class.  If you omit a command
        # or specify a bad one, there will be an error.
        #
        parser.add_argument (
            "commands",
            nargs = "*",
            choices = [x for x in dir (System)
                       if hasattr (getattr (System, x), "command")])

        # Place results into options variable
        options = parser.parse_args (args)

        # Internal function to show a value
        def show (name, value, default_value, alt_suffix=None):
            suffix = ""
            if (default_value is not None and value != default_value):
                suffix = " (default {})".format (default_value)
            elif (alt_suffix):
                suffix = " ({})".format (alt_suffix)
            print ("    {0:15}: {1}{2}".format (name, value, suffix))

        # If verbose, dump config options gathered
        if (options.verbose):
            # Turn options into a dictionary and iterate
            print ("Parsed command-line options: ")
            option_dict = vars (options)
            for key in sorted (option_dict):
                # Get default value for option
                default_value = parser.get_default (key)
                value = getattr (options, key) # option_dict[key]
                show (key, value, default_value)
            if len(options.commands) > 1:
                print ("Parsed command-line commands:")
                for arg in options.commands:
                    show ("argument", arg, None)

        # Optionally read configuration file
        if (not options.noconfig):
            # Read options
            if (options.verbose):
                print ("Reading config file {}".format (options.config))
            config = ConfigParser ()
            config.read (options.config)

            # Get desired profile, creating if necessary
            if (options.profile != "DEFAULT" and not config.has_section (options.profile)):
                config.add_section (options.profile)

            if (options.profile == "DEFAULT"):
                profile = config.defaults ()
            else:
                profile = {key: config.get (options.profile, key) for key in config.options (options.profile)}

            if (options.verbose):
                for key in profile:
                    show (key, profile[key],
                          config.defaults ()[key] if key in config.defaults() else None)

            # Override missing command line options with config file values
            if (options.verbose):
                print ("Options in effect:")
            for key in defaults:
                if (not hasattr (options, key) and not key in profile):
                    # Missing everywhere, use default value
                    if (key == "dbport"):
                        setattr (options, key, int (defaults[key]))
                    else:
                        setattr (options, key, defaults[key])
                    if (options.verbose):
                        show (key, defaults[key], None, "from default value")
                elif (not hasattr (options, key)):
                    # Missing from command option only, use config file value
                    if (key == "dbport"):
                        # Integer option
                        setattr (options, key, int (profile[key]))
                    else:
                        # String option
                        setattr (options, key, profile[key])
                    if (options.verbose):
                        show (key, profile[key], None, "from config file")
                elif (options.verbose):
                    show (key, getattr (options, key), None, "from command line")

                # Prepopulate config file section from command line for profile save
                if (hasattr (options, key) and not key in profile):
                    config.set (options.profile, key, str (getattr (options, key)))

            # Save options
            if (options.save):
                # Save config file
                print ("Writing configuration file {}".format (options.config))
                with open (options.config, 'w') as configfile:
                    config.write (configfile)

        if (options.verbose):
            print (self.long_description)

        # Save the options for later use
        self.options = options

    def createSystem (self):
        '''
        Instantiate and return a System using the default and given options.
        '''
        return System (self.options)

def command (func):
    '''
    Tagging annotation for methods, adds the attribute "command" to the function.

    Used in the System class to designate which functions are commands, by
    applying an attribute to only those functions.  You can then iterate over
    all the functions in the class and figure out which ones are commands.

    Example:
        @command
        def f (self):
            pass
        hasattr (f, "command")    # True
    '''
    setattr (func, "command", None)
    return func

class System (object):
    '''
    The Winter system embodied as a single object that runs commands.
    '''
    def __init__ (self, options):
        self.options = options
        pass

    def runCommands (self):
        '''
        Iterate through user commands and perform them, which is actually just
        calling various methods of this class.
        '''
        for command in self.options.commands:
            if (hasattr (self, command)):
                getattr (self, command) ()
            else:
                raise Exception ("ERROR: unknown command {}".format (command))

    @command
    def run (self):
        '''
        Command to run Winter, launching all the parts based on database.

        Looks only in deployment collection.

        Finds web components:
            "component": "web"
        Expects its setup to contain bindAddress and port:
            "setup" : { "bindAddress" : "127.0.0.2", "port" : 80 }

        Finds notify components:
            "component": "notify"

        Finds daemon components:
            "component": "daemon"

        '''
        print ("Hello")

    @command
    def test_db_connection (self):
        '''Command to test the database connection.'''
        print ("Testing database connection, host {}, port {}, database {}".format (
            self.options.dbhost, self.options.dbport, self.options.dbname))
        try:
            # Make connection
            client = pymongo.MongoClient (
                host=self.options.dbhost, port=self.options.dbport)
            client.admin.command ('ping')
            print ("Connected without error:")
            # Get server information
            info = client.server_info ()
            print ("    server version {}".format (info['version']))
            # Get database and names of collections
            database = client[self.options.dbname]
            # Try authenticating against the database
            if (self.options.dbuser):
                print ("Authenticating as user {}".format (
                    self.options.dbuser))
                database.authenticate (self.options.dbuser, self.options.dbpassword)
                print ("    authenticated to database '{}' as user '{}'".format (self.options.dbname, self.options.dbuser))
            else:
                print ("Not using database authentication")
            # Show collections
            names = database.collection_names ()
            print ("Database '{}' has {} collections".format (
                self.options.dbname, len (names)))
            client.close ()
        except pymongo.errors.InvalidName as ex:
            print ("Invalid database name: {}".format (str (ex)))
        except Exception as ex:
            print ("Problem connecting: {}".format (str (ex)))

# Running modules as top-level scripts is an antipattern, use bin/snow instead
if __name__ == '__main__':
    pass
