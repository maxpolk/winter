'''
Setup file to create a distribution.

To create a source distribution, from this directory run:

    python setup.py sdist --formats=gztar,zip

    The result is a dist directory containing the distribution, and
    a Winter.egg-info directory.

Otherwise you might want to run this to obtain an egg:

    python setup.py release sdist bdist_egg

To upload to PyPi, read more about register and upload at:
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
