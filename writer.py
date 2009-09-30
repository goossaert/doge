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
from rst_writer import RestructuredTextWriter

class Writer:

    buffer = []
    
    def __init__(self):
        self.rst = RestructuredTextWriter()
        pass

    # TODO check if this is possible to put all this in the node classes.
    def write(self, node_file):
        for node in node_file.content:
            if node.to_explore: 
                # TODO careful here, the order of docstring and definition is
                # up to every language and/or documentation system
                self.buffer.append(node.make_prototype() + '\n')
                node.parse_docstring()
                node.merge_docstring()
                docstring = node.make_docstring()
                #docstring = None
                if docstring:
                    self.buffer.append(docstring)
                self.write(node)
            else:
                self.buffer.append(node.content)
