"""
Python docstring generator.
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


from python import RestructuredTextFactory

class Padding:
    def __init__(self, node):
        indent_diff = node.indent_children - node.indent
        padding_name = ' ' * (node.indent_children + indent_diff)
        padding_description = ' ' * (node.indent_children + indent_diff * 2)
        padding = ' ' * node.indent_children


class Node:
    def __init__(self, indent=None, to_explore=False):
        self.indent = indent
        self.indent_children = None
        self.content = []
        self.sf = []
        self.sc = []
        self.parent = None
        self.to_explore = to_explore
        self.generator = RestructuredTextFactory()
        self.padding = None

    def find_parent_class(self):
        return self.parent.find_parent_class()


    def find_parent_function(self):
        return self.parent.find_parent_function()


    def make_docstring(self):
        pass


    def parse_docstring(self):
        pass


    def compute_padding(self):
        self.padding = Padding(self)



class FileNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent, to_explore=True) 
        self.descriptions = []
        self.docstring = []
        self.parameters = {}
        self.types = {}

    def find_parent_function(self):
        return None

    def make_docstring(self):
        return self.generator.make_docstring_file(self)

    def parse_docstring(self):
        return self.generator.parse_docstring_file(self)


class ClassNode(Node):
    def __init__(self, indent=None, name=None, definition=None):
        Node.__init__(self, indent, to_explore=True) 
        self.name = name
        self.definition = definition
        self.variables_class = {}
        self.variables_instance = {}
        self.types_class = {}
        self.types_instance = {}
        self.descriptions = []
        self.docstring = []

    def find_parent_class(self):
        return self


    def make_docstring(self):
        return self.generator.make_docstring_class(self)


    def make_prototype(self):
        return self.generator.make_prototype_class(self)
         

    def parse_docstring(self):
        return self.generator.parse_docstring_class(self)



class FunctionNode(Node):
    def __init__(self, indent=None, name=None, definition=None):
        Node.__init__(self, indent, to_explore=True) 
        self.name = name
        self.definition = definition
        self.parameters = {}
        self.types = {}
        self.descriptions = []
        self.docstring = []


    def find_parent_function(self):
        return self


    def make_docstring(self):
        return self.generator.make_docstring_function(self)


    def make_prototype(self):
        return self.generator.make_prototype_function(self)


    def parse_docstring(self):
        return self.generator.parse_docstring_function(self)
         

         
class CodeNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 



class CommentNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 

