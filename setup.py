'''
Setup file to create a distribution.

Python 2 is not supported!  It is a different language, with a different
library, and different syntax.  No point diluting effort supporting
multiple languages when one is just fine.  Please don't port to Python 2,
instead, please try using Python 3.  Pushing for Python 2 is wasted effort
for you AND OTHERS, for no gain whatsoever.  Don't do that.

To create a source distribution, from this directory run the following which
creates a dist directory containing the distribution, and a Winter.egg-info
directory:

    python3 setup.py sdist --formats=gztar,zip

Instead of "sdist" above, see the list of other standard commands with:

    python3 setup.py --help-commands

To upload to PyPi, read more about the "register" and "upload" commands at:
    http://pythonhosted.org/setuptools/setuptools.html#developer-s-guide

This file is part of Winter, a wiki-based computing platform.
Copyright (C) 2012  Max Polk <maxpolk@gmail.com>
'''
from setuptools import setup, find_packages

# Pick what to install
import sys
if sys.version_info[0] == 2:
    print ("Python 2 is not supported, please use Python 3")
    exit (1)
elif sys.version_info[0] == 3:
    base_dir = 'python3'

# We need to use the correct path for packages
import os
sys.path.append (os.path.join (os.path.dirname (__file__), base_dir))

import winter

setup (
    name=winter.software_name,
    version=winter.software_version,
    packages = ['winter', 'winter.test'],
    package_dir = {
        'winter': os.path.join (base_dir, 'winter'),
        'winter.test': os.path.join (base_dir, 'winter', 'test')
    },
    scripts = [os.path.join (base_dir, 'bin', 'runtests'),
               os.path.join (base_dir, 'bin', 'snow')],
    install_requires = ['bottle'],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
    # metadata for upload to PyPI
    author = "Max Polk",
    author_email = "maxpolk@gmail.com",
    description = winter.software_description,
    license = winter.software_abbreviation_license,
    keywords = "wiki",
    url = "http://winter.maxpolk.org/",   # project home page
    long_description = winter.software_long_description,
    # could also include long_description, download_url, classifiers, etc.
)
