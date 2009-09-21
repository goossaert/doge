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

import io
import re

from node import *

class Parser:
    pattern_indent = re.compile(
        r"""
        (?P<indent>[\s]*)
        .*?
        """, re.VERBOSE | re.DOTALL)


    pattern_class = re.compile(
        r"""
        (?P<indent>[\s]*?)
        class[\s]*?
        (?P<name>[_\w]*?)
            (\(
            (?P<definition>[\s\,\w\=]*)
            \))?
        [\s]*?[:][\s]*?
        """, re.VERBOSE | re.DOTALL)


    pattern_function = re.compile(
        r"""
        (?P<indent>[\s]*?)
        def[\s]*?
        (?P<name>[_\w]*?)
            \(
            (?P<definition>[\s\,\w\=]*)
            \)
        [\s]*?[:][\s]*?
        """, re.VERBOSE | re.DOTALL)


    pattern_assignment = re.compile(
        r"""
        (?P<indent>[\s]*?)
        (?P<name>[_\w]*?)
        [\s]*?[=][\s]*.*?
        """, re.VERBOSE | re.DOTALL)


    pattern_self = re.compile(
        r"""
        (?P<indent>[\s]*?)
        (self[.])
        (?P<name>[_\w]*?)
        [\s]*?[=][\s]*.*?
        """, re.VERBOSE | re.DOTALL)


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
                if line.strip().endswith('"""'):
                    # Exiting docstrings
                    in_docstring = False
                continue  

            if self.nodes[-1].indent_children == None and line.strip() != '':
                indent = self.pattern_indent.match(line).group('indent')
                self.nodes[-1].indent_children = len(indent)

                if line.strip().startswith('"""'):
                    # Entering docstrings
                    self.nodes[-1].docstring.append(line)
                    if len(line.strip()) < 6 or not line.strip().endswith('"""'):
                        # If this is not a one line docstring, then switch the flag
                        in_docstring = True 
                    continue

            node = None
            match = None
            if self.pattern_class.match(line):
                match = self.pattern_class.match(line)
                node = ClassNode()
            elif self.pattern_function.match(line):
                match = self.pattern_function.match(line)
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


    # TODO check if this is possible to put all this in the node classes.
    def build_structure(self):
        stack = [self.node_file] 
        while stack:
            node_parent = stack.pop()
            for node in node_parent.content:
                if node.to_explore:
                    stack.append(node)
                else: 
                    match_self = self.pattern_self.match(node.content)
                    if match_self:
                        node_class = node.find_parent_class()
                        node_class.variables_instance[match_self.group('name')] = ''

                    match_assignment = self.pattern_assignment.match(node.content)
                    if match_assignment and isinstance(node_parent, ClassNode):
                            node_parent.variables_class[match_assignment.group('name')] = ''
                            # TODO handle return
                            # TODO handle raise
                            pass
                    
                    
            if isinstance(node_parent, FunctionNode):
                parameters = re.split('[^\w=]+', node_parent.definition)
                for parameter in parameters:
                    if parameter and parameter != 'self':
                        name = re.split('[=]+', parameter)
                        node_parent.parameters[name[0]] = ''

                #fill parameters
                pass
