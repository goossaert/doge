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


# TODO: why writing the re-building the prototypes?
#       better just to paste the codenodes
class PythonLang:

    def make_prototype_class(self, node):
        #print 'class def:', node.definition
        return node.definition
        #base_classes = '(' + node.parents + ')' if node.parents else ''
        #return node.indent * ' ' + 'class ' + node.name + base_classes + ':'


    def make_prototype_function(self, node):
        #print 'fct def:', node.definition
        return node.definition
        #return node.indent * ' ' + 'def ' + node.name + '(' + node.arguments + ')' + ':'



class PythonParser:

    def __init__(self):
        pass

    def _pop_stack(self, stack, node):
        while stack and stack[-1].indent >= node.indent:
            print 'pop', stack[-1], stack[-1].indent, '| call:', node, node.indent
            del stack[-1]


    # TODO some operations can be put into methods to reduce
    # the size of the read_file method
    def read_file(self, file):
        stack = []
        node_file = FileNode(-1)
        stack.append(node_file)
        #node_file = None

        in_comment = False
        comments = []
        in_docstring = False
        docstring = []
        definition = []
        for line in file:
            if in_docstring:
                # Handling docstrings
                #nodes[-1].docstring.append(line)
                docstring.append(line)
                # TODO beware with endswith: maybe there is a \n at the very end
                if line.strip().endswith('"""'):
                    # Exiting docstrings
                    stack[-1].block_after = docstring[:]
                    docstring = []
                    in_docstring = False
                continue  

            if in_comment and not line.strip() \
              or line.lstrip().startswith('#'):
                in_comment = True
                comments.append(line)
                continue
            else:
                in_comment = False

            if stack[-1].indent_children == None and line.strip() != '':
                indent = python_pattern.indent.match(line).group('indent')
                stack[-1].indent_children = len(indent)
                stack[-1].compute_padding()

                if line.strip().startswith('"""'):
                    # Entering docstrings
                    #nodes[-1].docstring.append(line)
                    if len(line.strip()) < 6 or not line.strip().endswith('"""'):
                        # If this is not a one line docstring, then save and switch the flag
                        docstring.append(line)
                        in_docstring = True 
                    else:
                        stack[-1].block_after = [line]
                    continue

            # Bufferize definition lists
            if definition \
              or any(line.lstrip().startswith(s) for s in ['def ', 'class ']):
                definition += [line] 
                if not line.rstrip().endswith(':'):
                    continue

            # Definition done buffering, handle it
            node = None
            match = None
            listname = None
            definition = ''.join([line for line in definition])
            if python_pattern.class_.match(definition):
                match = python_pattern.class_.match(definition)
                node = ClassNode()
                listname = 'parents'
            elif python_pattern.function.match(definition):
                match = python_pattern.function.match(definition)
                node = FunctionNode()
                listname = 'arguments'

            if node:
                # Filling the node
                node.definition = definition # save the whole definition
                node.indent = len(match.group('indent'))
                node.name = match.group('name')
                setattr(node, listname, match.group(listname))
                node.block_before = comments
                print 'save before', comments

                # Modifying the state of the parser
                self._pop_stack(stack, node)
                node.parent = stack[-1]
                stack[-1].content.append(node)
                stack.append(node)
            else:
                #node_code = CodeNode(-1)
                #node_code.content = line
                #node_code.parent = nodes[-1]
                #nodes[-1].content.append(node_code)
                lines = comments + [line]

                for l in lines:
                    node_code = CodeNode(-1)
                    match = python_pattern.indent.match(l)
                    node_code.indent = len(match.group('indent'))
                    #print 'CODE:', node_code.indent, line.rstrip()
                    node_code.content = l
                    if line.strip(): # empty lines can mess the stack up
                        self._pop_stack(stack, node_code)
                    node_code.parent = stack[-1]
                    stack[-1].content.append(node_code)

            # prepare for next iteration
            definition = [] 
            comments = []

        # TODO: find a better way to do that (set correct indent in the description)
        node_file.indent = -4
        node_file.indent_children = 0
        node_file.compute_padding()

        return node_file


    # TODO: to delete
    #def _print(self, node):
    #    if isinstance(node, FileNode) or isinstance(node, ClassNode) or isinstance(node, FunctionNode):
    #        for sub in node.content:
    #            self._print(sub)


    # TODO: to delete
    #def print_file(self):
    #    self._print(node_file)


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
            print 'node', title, node_current, node_parent
            section = node_parent.sc.find_section(title)
            if not section:
            # Description
            # Note: this code comes rom rst_reader.py/_add_description
                section = SBSectionDescription(node_parent.padding, title)
                description = SBText(node_parent.padding, ['']) # [] used to be ''
                section.sd.append(description)
                node_parent.sc.sd.append(section)



    # TODO check if this is possible to put all this in the node classes.
    # TODO handle return
    # TODO handle raise
    def build_structure(self, node_file):
        stack = [node_file] 
        while stack:
            node_parent = stack.pop()
            for node in node_parent.content:
                if node.to_explore:
                    stack.append(node)
                else:
                    # All non-explorable node (mostly CodeNodes)
                    node_class = node.find_parent_class()# if node != None else None

                    if node_class:
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

                    # Module variable
                    if isinstance(node_parent, FileNode):
                        self._handle_section_parameter(python_pattern.assignment,
                                             node,
                                             node_parent,
                                             'Variables')

                    # Exceptions
                    self._handle_section_parameter(python_pattern.exception,
                                         node,
                                         node_parent,
                                         'Exceptions')

                    # Return and yield
                    self._handle_section_description(python_pattern.return_,
                                         node,
                                         node_parent,
                                         'Return')
                   
            # Function prototypes
            # TODO: factorize with the code of self._handle_section
            if isinstance(node_parent, FunctionNode):
                section = SBSectionParameter(node_parent.padding, 'Parameters')
                node_parent.sc.sd.append(section)
                parameters = re.split('[^\w=]+', node_parent.arguments)
                for parameter in parameters:
                    if parameter and parameter != 'self':
                        name = re.split('[=]+', parameter)[0]
                        section.parameters[name] = SBParameter(node.padding, name)
                        #description = SBText(node.padding)
                        #section.parameters[name].sd.append(description)
