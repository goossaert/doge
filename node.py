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
        return ''


class FileNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent, to_explore=True) 


class ClassNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent, to_explore=True) 
        self.variables_class = {}
        self.variables_instance = {}
        self.description = ''

    def find_parent_class(self):
        return self

    def make_docstring(self):
        return 'class'


class FunctionNode(Node):
    def __init__(self, indent=None, definition=None):
        Node.__init__(self, indent, to_explore=True) 
        self.definition = definition
        self.parameters = {}
        self.description = ''


    def find_parent_function(self):
        return self


    def make_docstring(self):
        if not self.parameters:
            return ''

        doc_parameter = '%s%s\n\
                         %s%s\n'.replace(' ','')

        doc_function = '%(indent)s"""\n\
                        %(indent)s%(description)s\n\
                        \n\
                        %(indent)s:Parameters:\n\
                        %(parameters)s\n\
                        %(indent)s"""'.replace(' ','')

        diff = self.indent_children - self.indent
        print self.indent_children, self.indent
        print 'diff', diff
        indent_name = '-' * (self.indent + diff)
        indent_description = '-' * (self.indent + diff * 2)
        indent = '-' * self.indent

        parameters = ''

        parameters = [doc_parameter % (indent_name, name, indent_description, description) for name, description in self.parameters.items()]
        print 'PARAMS:', ''.join(parameters)

        return doc_function % {'indent': indent, 'description': self.description, 'parameters': ''.join(parameters)}
         
         
class CodeNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 



class CommentNode(Node):
    def __init__(self, indent=None):
        Node.__init__(self, indent) 

