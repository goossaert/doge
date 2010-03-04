"""
Python regular expression patterns.
"""
__docformat__ = "restructuredtext en"

## Copyright (c) 2009 Emmanuel Goossaert 
##
## This file is part of pydoge.
##
## pydoge is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## pydoge is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with pydoge.  If not, see <http://www.gnu.org/licenses/>.

import re


indent = re.compile(
    r"""
    (?P<indent>[\s]*)
    .*?
    """, re.VERBOSE | re.DOTALL)


section = re.compile(
    r"""
    (?P<indent>[\s]*)
    [:|@]
    (?P<title>[\w]*)
    ([\s]*(?P<option>[\w]*))?
    [:]
    ([\s]*(?P<content>.*))?
    [\s]*
    """, re.VERBOSE | re.DOTALL)



class_ = re.compile(
    r"""
    (?P<indent>[\s]*?)
    class[ ]*?
    (?P<name>[_\w]*?)
        (\(
        (?P<definition>[\s\,\w\=]*)
        \))?
    [\s]*?[:,][\s]*?
    """, re.VERBOSE | re.DOTALL)


function = re.compile(
    r"""
    (?P<indent>[\s]*?)
    def[ ]*?
    (?P<name>[_\w]*?)
        (\(
        (?P<definition>[\s\,\w\=]*)
        \))?
    [\s]*?[:,][\s]*?
    """, re.VERBOSE | re.DOTALL)


assignment = re.compile(
    r"""
    (?P<indent>[\s]*?)
    (?P<name>[_\w]*?)
    [\s]*?[=][\s]*.*?
    """, re.VERBOSE | re.DOTALL)


self = re.compile(
    r"""
    (?P<indent>[\s]*?)
    (self[.])
    (?P<name>[_\w]*?)
    [\s]*?[=][\s]*.*?
    """, re.VERBOSE | re.DOTALL)


exception = re.compile(
    r"""
    (?P<indent>[\s]*)
    raise[\s]*
    (?P<name>[\w]*)
    """, re.VERBOSE | re.DOTALL)


return_ = re.compile(
    r"""
    (?P<indent>[\s]*)
    return[\s]*
    [^\s]+
    """, re.VERBOSE | re.DOTALL)
