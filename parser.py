import io
import re

from node import *

class Parser:
    pattern_class = re.compile(
        r"""
        (?P<indent>[\s]*?)
        class[ ].*?
        """, re.VERBOSE | re.DOTALL)

    pattern_function = re.compile(
        r"""
        (?P<indent>[\s]*?)
        def[ ].*?
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
                indent = self.pattern_class.match(line).group('indent') 
                node = ClassNode(len(indent))
            elif self.pattern_function.match(line):
                print 'function'
                indent = self.pattern_function.match(line).group('indent') 
                node = FunctionNode(len(indent))

            if node:
                self._pop_nodes(node)
                self.nodes[-1].content.append(node)
                self.nodes.append(node)

            node_code = CodeNode(-1)
            node_code.content = line
            self.nodes[-1].content.append(node_code)


    def _print(self, node):
        print node, node.indent
        print node.content
        if isinstance(node, FileNode) or isinstance(node, ClassNode) or isinstance(node, FunctionNode):
            for sub in node.content:
                self._print(sub)

    def print_file(self):
        self._print(self.node_file)
