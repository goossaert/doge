"""
Node system.
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


from rst_reader import RestructuredTextReader
from rst_writer import RestructuredTextWriter
from merger import Merger
from doc import *
from padding import Padding



class Node:
    reader = None
    writer = None
    lang = None

    def __init__(self, indent=None, to_explore=False):
        self.indent = indent
        self.indent_children = None
        self.content = []
        self.parent = None
        self.to_explore = to_explore
        self.merger = Merger()
        self.padding = None
        self.sf = None
        self.sc = None


    def find_parent_class(self):
        return self.parent.find_parent_class() if self.parent else None


    def find_parent_function(self):
        return self.parent.find_parent_function() if self.parent else None


    def make_docstring(self):
        #return ''.join([item.make_docstring() for item in self.sf.sd])
        return self.sc.make_docstring()
        pass


    def parse_docstring(self):
        pass


    def merge_docstring(self):
        pass


    def compute_padding(self):
        indent_diff = self.indent_children - self.indent
        indent_base = self.indent_children
        self.padding = Padding(indent_base, indent_diff)
        if self.sf:
            self.sf.padding = self.padding
        if self.sc:
            self.sc.padding = self.padding



class FileNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent, to_explore=True) 
        #self.descriptions = []
        self.docstring = []
        self.sf = SBFile()
        self.sc = SBFile()
        #self.parameters = {}
        #self.types = {}


    def find_parent_function(self):
        return None


    def make_docstring(self):
        #return self.sc.make_docstring(self)
        return self.sc.make_docstring()


    def parse_docstring(self):
        return self.reader.parse_docstring_file(self)


    def merge_docstring(self):
        #self.merger.merge_file(self.sf, self.sc)
        self.sc.swallow(self.sf)



class ClassNode(Node):
    def __init__(self, indent=None, name=None, definition=None):
        Node.__init__(self, indent, to_explore=True) 
        self.name = name
        self.definition = definition
        self.sf = SBClass()
        self.sc = SBClass()
        #self.variables_class = {}
        #self.variables_instance = {}
        #self.types_class = {}
        #self.types_instance = {}
        #self.descriptions = []
        self.docstring = []

    def find_parent_class(self):
        return self


    def make_docstring(self):
        return self.sc.make_docstring()
        

    def obs_make_docstring(self):
        return self.writer.make_docstring_class(self)


    def make_prototype(self):
        return self.lang.make_prototype_class(self)
         

    def parse_docstring(self):
        return self.reader.parse_docstring_class(self)


    def merge_docstring(self):
        #self.merger.merge_class(self.sf, self.sc)
        self.sc.swallow(self.sf)



class FunctionNode(Node):
    def __init__(self, indent=None, name=None, definition=None):
        Node.__init__(self, indent, to_explore=True) 
        self.name = name
        self.definition = definition
        #self.parameters = {}
        #self.types = {}
        #self.descriptions = []
        self.docstring = []
        self.sf = SBFunction()
        self.sc = SBFunction()


    def find_parent_function(self):
        return self


    def obs_make_docstring(self):
        return self.writer.make_docstring_function(self)


    def make_prototype(self):
        return self.lang.make_prototype_function(self)


    def parse_docstring(self):
        return self.reader.parse_docstring_function(self)
         

    def merge_docstring(self):
        #self.merger.merge_function(self.sf, self.sc)
        self.sc.swallow(self.sf)



class CodeNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 



class CommentNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 

