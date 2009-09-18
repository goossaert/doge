class Node:
    def __init__(self, indent=None):
        self.indent = indent
        self.content = []





class FileNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 



class ClassNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 


class FunctionNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 


class CodeNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 


class CommentNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 
