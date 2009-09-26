"""
Documentation class hierarchy.
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


def find_section(name, sections):
    for section in sections:
        #if (isinstance(section, SBSectionDescription) or isinstance(section, SBSectionParameter) ) and section.name == name:
        if isinstance(section, SBSection):
            print 'search:', section, '"' + section.name + '"', '"' + name + '"'
            if section.name == name:
                return section
    return None


# TODO delete the SB class hierarchy
class SB:
    def __init__(self, padding=None):
        self.padding = padding
        self.sd = []

    def make_docstring(self):
        return 'empty'


class SBParameter(SB):
    def __init__(self, padding=None, name=None, type=None):
        SB.__init__(self, padding)
        self.name = name
        self.type = type


class SBDescription(SB):
    def __init__(self, padding=None, text=[]):
        SB.__init__(self, padding)
        self.text = text


class SBSection(SB):
    def __init__(self, padding=None, name=None, option=None):
        SB.__init__(self, padding)
        self.name = name
        self.option = option


class SBSectionParameter(SBSection):
    def __init__(self, padding=None, name=None, option=None):
        SBSection.__init__(self, padding, name, option)
        self.parameters = {}


class SBSectionDescription(SBSection):
    def __init__(self, padding=None, name=None, option=None):
        SBSection.__init__(self, padding, name, option)



