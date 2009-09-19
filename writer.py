from node import *

class Writer:

    buffer = []
    
    def __init__(self):
        pass

    def write(self, node_file):
        for node in node_file.content:
            if node.to_explore: 
                self.buffer.append(node.make_prototype() + '\n')
                docstring = node.make_docstring()
                if docstring:
                    self.buffer.append(docstring)
                self.write(node)
            else:
                self.buffer.append(node.content)
