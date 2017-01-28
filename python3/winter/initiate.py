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
        Read and return parsed command-line options and command arguments.
        Command-line options override config file options.
        '''
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
            default = os.path.expanduser ("~/.winter"),
            help = "directory to be used for file cache [default: %(default)s]")

        # DB host: specify hostname where to find MongoDB database
        parser.add_argument (
            "--dbhost",
            default = '127.0.0.1',
            help = "hostname of MongoDB database [default: %(default)s]")

        # DB port: specify port number to MongoDB database
        parser.add_argument (
            "--dbport",
            default = 27017,
            type = int,
            help = "port number of MongoDB database [default: %(default)s]")

        # DB name: specify database name to use for MongoDB database
        parser.add_argument (
            "--dbname",
            default = 'winter',
            help = "database name to use inside MongoDB database [default: %(default)s]")

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

        # If verbose, dump config options gathered
        if (options.verbose):
            def show (name, value, default_value):
                suffix = ""
                if (default_value is not None and value != default_value):
                    suffix = " (default {})".format (default_value)
                print ("    {0:15}: {1}{2}".format (name, value, suffix))

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

            # Fill in defaults not already inside the config file
            option_dict = vars (options)
            for key in ("dbhost", "dbname", "dbport", "directory"):
                # Get default value for option
                default_value = parser.get_default (key)
                if (not config.has_option ("DEFAULT", key)):
                    if (options.verbose):
                        print ("Adding missing default {} to value {}".format (
                            key, default_value))
                    config.set ("DEFAULT", key, str (default_value))

            # Get desired profile, creating if necessary
            if (options.profile != "DEFAULT" and not config.has_section (options.profile)):
                config.add_section (options.profile)
            if (options.profile == "DEFAULT"):
                profile = config.defaults ()
            else:
                profile = config.options (options.profile)

            # Dump profile before command-line overrides
            if (options.verbose):
                print ("Profile values for section {}:".format (options.profile))
                for key in profile:
                    print ("    {} = {}".format (key, config.get (options.profile, key)))

            # Let command options override config file values
            for key in ("dbhost", "dbname", "dbport", "directory"):
                value = str (getattr (options, key))
                config_value = config.get (options.profile, key)
                config_default_value = config.get ("DEFAULT", key)
                if (options.profile == "DEFAULT" and config_default_value != value):
                    if (options.verbose):
                        print ("Overriding default option with command-line option {} = {}".format (key, value))
                    config.set (options.profile, key, value)
                if (options.profile != "DEFAULT" and str (parser.get_default (key)) != value and config_value != value):
                    if (options.verbose):
                        print ("Overriding config option with command-line option {} = {}".format (key, value))
                    config.set (options.profile, key, value)

            # Dump profile with overrides, the final values to use
            if (options.verbose):
                print ("Profile values to use:")
                for key in profile:
                    print ("    {} = {}".format (key, config.get (options.profile, key)))

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
            names = database.collection_names ()
            print ("    database '{}' has {} collections".format (
                self.options.dbname, len (names)))
            client.close ()
        except pymongo.errors.InvalidName as ex:
            print ("Invalid database name: {}".format (str (ex)))
        except Exception as ex:
            print ("Problem connecting: {}".format (str (ex)))

# Running modules as top-level scripts is an antipattern, use bin/snow instead
if __name__ == '__main__':
    pass
