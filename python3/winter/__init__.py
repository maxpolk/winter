# This file is part of Winter, a wiki-based computing platform.
# Copyright (C) 2012,2013,2014,2015  Max Polk <maxpolk@gmail.com>
# License located at http://www.gnu.org/licenses/agpl-3.0.html
'''
This is the main package of Winter.
'''

# EACH RELEASE MODIFY: __software_date__ and __software_type__

# Last two digits of year, followed by two digit month.
# YYMM of release date, restrict to [0-9]{4} (used by setup.py)
__software_date__ = "1607"

# Type of release, use "a" for alpha, "b" for beta, "c" for release candidate,
# and "" (the empty string) or "final" for final release version.
__software_type__ = "a"

# Name of this software
software_name = "Winter"

# Sofware version concatenates date and type (list of versions sort perfectly)
software_version = "{}.{}".format (__software_date__, __software_type__)

# Short description of this software
software_description = "a wiki-based computing platform"

# Long description of this software
software_long_description = '''
Winter is a computing platform based on a wiki whose pages are code or data, combinined to form arbitrary content.  The code can be any domain-specific language.  The data can either be immediate information, or else a reference to external information, such as a web API, a web resource like a news feed, a database lookup, a directory of files, local system information, the output of a command or program, or anything else.

The goal of Winter is to bring software development to everyone.  No tool is needed other than a browser, and no skill is needed other than an ability to type simple text to morph data.  By emphasizing smaller steps and then combining them, no one page is ever complex.  Testing and releasing are built-in to complete the platform.

This project is licensed under version 3 of the GNU Affero General Public License, which you can read here: http://www.gnu.org/licenses/agpl-3.0.html
'''

# License
software_license = '''
This file is part of Winter, a wiki-based computing platform.
Copyright (C) 2015  Max Polk <maxpolk@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

software_short_license = '''
Copyright (C) 2015  Max Polk <maxpolk@gmail.com>
License located at http://www.gnu.org/licenses/agpl-3.0.html
'''

software_abbreviation_license = "GNU AGPL"
