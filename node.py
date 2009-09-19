"""
pydoge - python docstring generator 
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

class Node:
    def __init__(self, indent=None, to_explore=False):
        self.indent = indent
        self.indent_children = None
        self.content = []
        self.parent = None
        self.to_explore = to_explore

    def find_parent_class(self):
        return self.parent.find_parent_class()

    def find_parent_function(self):
        return self.parent.find_parent_function()

    def make_docstring(self):
        return None


class FileNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent, to_explore=True) 

    def find_parent_function(self):
        return None


class ClassNode(Node):
    def __init__(self, indent=None, name=None, definition=None):
        Node.__init__(self, indent, to_explore=True) 
        self.name = name
        self.definition = definition
        self.variables_class = {}
        self.variables_instance = {}
        self.description = ''

    def find_parent_class(self):
        return self


    def make_docstring(self):
        if not self.variables_class and not self.variables_instance:
            return ''

        doc_variable = '-%s%s\n\
                        -%s%s\n'.replace(' ','')

        doc_section = '\n\
                        -%(indent)s:%(section)s:\n\
                        -%(variables)s'.replace(' ','')

        doc_function = '-%(indent)s"""\n\
                        -%(indent)s%(description)s%(content)s\
                        -%(indent)s"""\n'.replace(' ', '')

        #

        # TODO factorize with make_docstring for functions
        diff = self.indent_children - self.indent
        indent_name = ' ' * (self.indent_children + diff)
        indent_description = ' ' * (self.indent_children + diff * 2)
        indent = ' ' * self.indent_children

        var_class = [doc_variable % (indent_name, name, indent_description, description) for name, description in self.variables_class.items()]
        var_class_content = doc_section % {'indent': indent, 'section': 'CVariable', 'variables': ''.join(var_class)}

        var_instance = [doc_variable % (indent_name, name, indent_description, description) for name, description in self.variables_instance.items()]
        var_instance_content = doc_section % {'indent': indent, 'section': 'IVariable', 'variables': ''.join(var_instance)}

        content = ''
        if var_class:
            content += var_class_content

        if var_instance:
            content += var_instance_content

        return doc_function % {'indent': indent, 'description': self.description, 'content': content}


    def make_prototype(self):
        base_classes = '(' + self.definition + ')' if self.definition else ''
        return self.indent * ' ' + 'class ' + self.name + base_classes + ':'
         


class FunctionNode(Node):
    def __init__(self, indent=None, name=None, definition=None):
        Node.__init__(self, indent, to_explore=True) 
        self.name = name
        self.definition = definition
        self.parameters = {}
        self.description = ''


    def find_parent_function(self):
        return self


    def make_docstring(self):
        if not self.parameters:
            return ''

        doc_parameter = '%s%s\n\
                         %s%s\n\n'.replace(' ','')

        doc_function = '%(indent)s"""\n\
                        %(indent)s%(description)s\n\
                        \n\
                        %(indent)s:Parameters:\n\
                        %(parameters)s\n\
                        %(indent)s"""\n'.replace(' ','')

        diff = self.indent_children - self.indent
        indent_name = ' ' * (self.indent_children + diff)
        indent_description = ' ' * (self.indent_children + diff * 2)
        indent = ' ' * self.indent_children

        parameters = [doc_parameter % (indent_name, name, indent_description, description) for name, description in self.parameters.items()]

        return doc_function % {'indent': indent, 'description': self.description, 'parameters': ''.join(parameters)}

    def make_prototype(self):
        return self.indent * ' ' + 'def ' + self.name + '(' + self.definition + ')' + ':'
         
         
class CodeNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 



class CommentNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 

