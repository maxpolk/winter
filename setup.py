'''
Setup file to create a distribution.

Based on whether you are using Python 2 or 3, a different root directory
is picked.  This lets the burden of version compatibility rest upon the
package authors and maintainers, rather than upon the users.

To create a source distribution, from this directory run either of these
to obtain a dist directory containing the distribution, and a Winter.egg-info
directory:

    python setup.py sdist --formats=gztar,zip
    python3 setup.py sdist --formats=gztar,zip

Instead of "sdist" above, see the list of other standard commands with:

    python setup.py --help-commands
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
    base_dir = 'python2'
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
