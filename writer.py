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

from node import *

class Writer:


    def __init__(self):
        self.buffer = []


    # TODO check if this is possible to put all this in the node classes.
    def write(self, node):
        #self.buffer = []

        if node.to_explore:
            self.buffer.extend(node.block_before)
            if hasattr(node, 'make_prototype'):
                self.buffer.append(node.make_prototype())# + '\n')

            # TODO careful here, the order of docstring and definition is
            # up to every language and/or documentation system
            node.parse_docstring()
            node.merge_docstring()
            docstring = node.make_docstring()
            if docstring:
                self.buffer.append(docstring)

            # Go for children nodes
            for node_child in node.content:
                self.write(node_child)
        else:
            self.buffer.append(node.content)

