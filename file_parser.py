import io
import re

from node import *

class Parser:
    pattern_indent = re.compile(
        r"""
        (?P<indent>[\s]*?)
        .*?
        """, re.VERBOSE | re.DOTALL)

    pattern_class = re.compile(
        r"""
        (?P<indent>[\s]*?)
        class[ ].*?
        """, re.VERBOSE | re.DOTALL)

    pattern_function = re.compile(
        r"""
        (?P<indent>[\s]*?)
        def[\s]*?
        (?P<name>[_\w]*?)
            \(
            (?P<parameters>[\s\,\w\=]*)
            \)
        [\s]*?[:][\s]*?
        """, re.VERBOSE | re.DOTALL)

    pattern_assignment = re.compile(
        r"""
        (?P<indent>[\s]*?)
        (?P<name>[_\w]*?)
        [\s]*?[=][\s]*.*?
        """, re.VERBOSE | re.DOTALL)
        #([\s]*?#[\s]*?)

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

        for line in file:
            #print 'handling:', line
            node = None
            if self.pattern_class.match(line):
                print 'class'
                match = self.pattern_class.match(line)
                indent = match.group('indent') 
                node = ClassNode(len(indent))
            elif self.pattern_function.match(line):
                print 'function'
                match = self.pattern_function.match(line)
                indent = match.group('indent') 
                definition = match.group('parameters')
                node = FunctionNode(len(indent), definition)

            if node:
                self._pop_nodes(node)
                node.parent = self.nodes[-1]
                self.nodes[-1].content.append(node)
                self.nodes.append(node)
            else:
                node_code = CodeNode(-1)
                node_code.content = line
                node_code.parent = self.nodes[-1]
                self.nodes[-1].content.append(node_code)
                if self.nodes[-1].indent_children == None and not line.strip():
                    print 'line', line
                    indent = self.pattern_indent.match(line).group('indent')
                    self.nodes[-1].indent_children = len(indent)


    def _print(self, node):
        print node, node.indent
        print node.content
        if isinstance(node, FileNode) or isinstance(node, ClassNode) or isinstance(node, FunctionNode):
            for sub in node.content:
                self._print(sub)


    def print_file(self):
        self._print(self.node_file)


    def build_structure(self):
        print 'build'
        stack = [self.node_file] 
        while stack:
            node_parent = stack.pop()
            for node in node_parent.content:
                print node
                if node.to_explore:
                    stack.append(node)
                else: 
                    match_self = self.pattern_self.match(node.content)
                    if match_self:
                        node_class = node.find_parent_class()
                        node_class.variables_instance[match_self.group('name')] = ''
                        print 'instance', match_self.group('name')

                    match_assignment = self.pattern_assignment.match(node.content)
                    if match_assignment and isinstance(node_parent, ClassNode):
                            node_parent.variables_class[match_assignment.group('name')] = ''
                            print 'class', match_assignment.group('name')
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
