"""
Python language module.
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

import io
import re

import doc
import python_pattern

from doc import *
from node import *


class PythonLang:

    def make_prototype_class(self, node):
        base_classes = '(' + node.definition + ')' if node.definition else ''
        return node.indent * ' ' + 'class ' + node.name + base_classes + ':'


    def make_prototype_function(self, node):
        return node.indent * ' ' + 'def ' + node.name + '(' + node.definition + ')' + ':'



class PythonParser:

    def __init__(self):
        self.module = None
        self.nodes = []
        self.node_file = None


    def _pop_nodes(self, node):
        while self.nodes and self.nodes[-1].indent >= node.indent:
            del self.nodes[-1]


    def read_file(self, name_file):
        file = open(name_file, 'r')

        self.node_file = FileNode(-1)
        self.nodes.append(self.node_file)

        in_docstring = False
        for line in file:
            if in_docstring:
                # Handling docstrings
                self.nodes[-1].docstring.append(line)
                # TODO beware with endswith: maybe there is a \n at the very end
                if line.strip().endswith('"""'):
                    # Exiting docstrings
                    in_docstring = False
                continue  

            if self.nodes[-1].indent_children == None and line.strip() != '':
                indent = python_pattern.indent.match(line).group('indent')
                self.nodes[-1].indent_children = len(indent)
                self.nodes[-1].compute_padding()

                if line.strip().startswith('"""'):
                    # Entering docstrings
                    self.nodes[-1].docstring.append(line)
                    if len(line.strip()) < 6 or not line.strip().endswith('"""'):
                        # If this is not a one line docstring, then switch the flag
                        in_docstring = True 
                    continue

            node = None
            match = None
            if python_pattern.class_.match(line):
                match = python_pattern.class_.match(line)
                node = ClassNode()
            elif python_pattern.function.match(line):
                match = python_pattern.function.match(line)
                node = FunctionNode()

            if node:
                # Filling the node
                node.indent = len(match.group('indent'))
                node.name = match.group('name')
                node.definition = match.group('definition')
                
                # Modifying the state of the parser
                self._pop_nodes(node)
                node.parent = self.nodes[-1]
                self.nodes[-1].content.append(node)
                self.nodes.append(node)
            else:
                node_code = CodeNode(-1)
                node_code.content = line
                node_code.parent = self.nodes[-1]
                self.nodes[-1].content.append(node_code)



    def _print(self, node):
        if isinstance(node, FileNode) or isinstance(node, ClassNode) or isinstance(node, FunctionNode):
            for sub in node.content:
                self._print(sub)


    def print_file(self):
        self._print(self.node_file)


    def _handle_section_parameter(self, pattern, node_current, node_parent, title):
        match = pattern.match(node_current.content)
        if match:
            #try:
                # Parameters
                name = match.group('name')
                section = node_parent.sc.find_section(title)
                if not section:
                    section = SBSectionParameter(node_parent.padding, title)
                    # the current class is obviously a CodeNode, so the section
                    # is added to the parent which is a File, Class or Function
                    node_parent.sc.sd.append(section)
                section.parameters[name] = SBParameter(node_parent.padding, name)
                description = SBText(node_parent.padding)
                section.parameters[name].sd.append(description)
                # TODO add an empty description?


    def _handle_section_description(self, pattern, node_current, node_parent, title):
        match = pattern.match(node_current.content)
        if match:
                # Description
                # Note: this code comes rom rst_reader.py/_add_description
                section = SBSectionDescription(node_parent.padding, title)
                description = SBText(node_parent.padding, ['']) # [] used to be ''
                section.sd.append(description)
                node_parent.sc.sd.append(section)



    # TODO check if this is possible to put all this in the node classes.
    # TODO handle return
    # TODO handle raise
    def build_structure(self):
        stack = [self.node_file] 
        while stack:
            node_parent = stack.pop()
            for node in node_parent.content:
                if node.to_explore:
                    stack.append(node)
                else:
                    # All non-explorable node (mostly CodeNodes)
                    node_class = node.find_parent_class()# if node != None else None

                    # Instance variables
                    self._handle_section_parameter(python_pattern.self,
                                         node,
                                         node_class,
                                         'IVariables')

                    # Class variables
                    if isinstance(node_parent, ClassNode):
                        self._handle_section_parameter(python_pattern.assignment,
                                             node,
                                             node_class,
                                             'CVariables')

                    # Exceptions
                    self._handle_section_parameter(python_pattern.exception,
                                         node,
                                         node_parent,
                                         'Exceptions')

                    # Return
                    self._handle_section_description(python_pattern.return_,
                                         node,
                                         node_parent,
                                         'Return')
                   
            # Function prototypes
            # TODO: factorize with the code of self._handle_section
            if isinstance(node_parent, FunctionNode):
                section = SBSectionParameter(node_parent.padding, 'Parameters')
                node_parent.sc.sd.append(section)
                parameters = re.split('[^\w=]+', node_parent.definition)
                for parameter in parameters:
                    if parameter and parameter != 'self':
                        name = re.split('[=]+', parameter)[0]
                        section.parameters[name] = SBParameter(node.padding, name)
                        #description = SBText(node.padding)
                        #section.parameters[name].sd.append(description)
