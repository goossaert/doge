"""
Padding.
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



class Padding:
    def __init__(self, base, diff):
        self.base = base
        self.diff = diff
        #self.indent_diff = node.indent_children - node.indent
        #self.name = ' ' * (node.indent_children + self.indent_diff)
        #self.description = ' ' * (node.indent_children + self.indent_diff * 2)
        #self.children = ' ' * node.indent_children

    def padding(self, level=0):
        return ' ' * (self.base + self.diff * level)

