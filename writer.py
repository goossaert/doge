from node import *

class Writer:
    
    def __init__(self):
        pass

    def write(self, node_file):
        for node in node_file.content:
            if node.to_explore: 
                docstring = node.make_docstring()
                print node, docstring
                self.write(node)
