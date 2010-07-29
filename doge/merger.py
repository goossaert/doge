"""
Python docstring writer.
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

import doc

from node import *


class Merger:

    def __init__(self):
        pass


    def _merge_parameters(self, name, sb_src, sb_dest):
        #section_src = sb_src.find_section(name)
        #section_dest = sb_dest.find_section(name)
        #if section_src and section_dest: 
        #    section_dest.parameters.update(section_src.parameters) 
            #section_dest.parameters = section_src.parameters
        pass


    def merge_function(self, sb_src, sb_dest):
        self._merge_parameters('Parameters', sb_src, sb_dest)


    def merge_file(self, sb_src, sb_dest):
        self._merge_parameters('Parameters', sb_src, sb_dest)


    def merge_class(self, sb_src, sb_dest):
        self._merge_parameters('CVariables', sb_src, sb_dest)
        pass
        self._merge_parameters('IVariables', sb_src, sb_dest)

