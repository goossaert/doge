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


import re


pattern_indent = re.compile(
    r"""
    (?P<indent>[\s]*)
    .*?
    """, re.VERBOSE | re.DOTALL)


pattern_sequence = re.compile(
    r"""
    (?P<indent>[\s]*)
    [:]
    (?P<title>[\w]*)
    ([\s]*(?P<option>[\w]*))?
    [:]
    .*?
    """, re.VERBOSE | re.DOTALL)





class PythonFactory:
    def __init__(self):
        pass


    def make_docstring_file(self, node):
        return ''


    def make_docstring_class(self, node):
        if not node.variables_class and not node.variables_instance:
            return ''

        doc_variable = '-%s%s\n\
                        -%s%s\n'.replace(' ','')

        doc_section = '\n\
                        -%(indent)s:%(section)s:\n\
                        -%(variables)s'.replace(' ','')

        doc_function = '-%(indent)s"""\n\
                        -%(indent)s%(description)s%(content)s\
                        -%(indent)s"""\n'.replace(' ', '')

        # TODO factorize with make_docstring for functions
        diff = node.indent_children - node.indent
        indent_name = ' ' * (node.indent_children + diff)
        indent_description = ' ' * (node.indent_children + diff * 2)
        indent = ' ' * node.indent_children

        var_class = [doc_variable % (indent_name, name, indent_description, description) for name, description in node.variables_class.items()]
        var_class_content = doc_section % {'indent': indent,
                                           'section': 'CVariable',
                                           'variables': ''.join(var_class)}

        var_instance = [doc_variable % (indent_name, name, indent_description, description) for name, description in node.variables_instance.items()]
        var_instance_content = doc_section % {'indent': indent,
                                              'section': 'IVariable',
                                              'variables': ''.join(var_instance)}

        content = ''
        if var_class:
            content += var_class_content

        if var_instance:
            content += var_instance_content

        return doc_function % {'indent': indent,
                               'description': node.description,
                               'content': content}


    def make_docstring_function(self, node):
        if not node.parameters:
            return ''

        doc_parameter = '%s%s\n\
                         %s%s\n\n'.replace(' ','')

        doc_function = '%(indent)s"""\n\
                        %(indent)s%(description)s\n\
                        \n\
                        %(indent)s:Parameters:\n\
                        %(parameters)s\n\
                        %(indent)s"""\n'.replace(' ','')

        indent_diff = node.indent_children - node.indent
        indent_name = ' ' * (node.indent_children + indent_diff)
        indent_description = ' ' * (node.indent_children + indent_diff * 2)
        indent = ' ' * node.indent_children

        parameters = [doc_parameter % (indent_name, name, indent_description, description) for name, description in node.parameters.items()]

        return doc_function % {'indent': indent,
                               'description': node.description,
                               'parameters': ''.join(parameters)}


    def parse_docstring_file(self, node):
        self.parse_sections(node, node.docstring)


    def parse_docstring_class(self, node):
        self.parse_sections(node, node.docstring)


    def parse_docstring_function(self, node):
        self.parse_sections(node, node.docstring)


    def parse_sections(self, node, docstring):
        sequences = {}
        id_sequence = None
        option_current = None
        sequence_current = None
        sequences_text = ['Returns', 'Raises']
        sequences_parameter = ['IVariables', 'CVariables', 'Parameters']

        for id_line, line in enumerate(docstring):
            # look for sequences and end of docstring
            if line.strip().startswith(':') and line.strip().endswith(':') \
              or line.strip() == '"""':
                # sequence detected
                if sequence_current:
                    # already in a sequence, hence we have to treat it before
                    # setting up the new one
                    parser = self.parse_sequence_text if sequence_current in sequences_text else self.parse_sequence_parameter
                    content = parser(node, docstring[id_sequence + 1:id_line])
                    content.append(option_current)
                    sequences[sequence_current] = content
                     
                match = pattern_sequence.match(line)
                if match:
                    sequence_current = match.group('title')
                    option_current = match.group('option')
                id_sequence = id_line
        pass



    def _strip_docstring(self, docstring):
        # skip the empty lines at the beginning of the docstring
        id_start = None
        for id_line, line in enumerate(docstring):
            if not line.strip():
                id_start = id_line + 1
            else:
                break
        return docstring[id_start:]


    def parse_sequence_text(self, node, docstring):
        docstring = self._strip_docstring(docstring)

        #indent_diff = node.indent_children - node.indent
        indent_diff = 4
        indent_description = len(pattern_indent.match(docstring[0]).group('indent'))
        description = ['']
        for line in docstring:
            indent_current = len(pattern_indent.match(line).group('indent'))
            if indent_current == indent_description:
                description = self._handle_description(indent_current,
                                                       indent_description,
                                                       line,
                                                       description)
        return [description]



    def parse_sequence_parameter(self, node, docstring):
        if not docstring:
            return {}

        docstring = self._strip_docstring(docstring)

        # initialize containers
        descriptions = {}
        types = {}

        #indent_diff = node.indent_children - node.indent
        indent_diff = 4
        indent_parameter = len(pattern_indent.match(docstring[0]).group('indent'))
        indent_description = indent_parameter + indent_diff 

        parameter = None
        for line in docstring:
            indent_current = len(pattern_indent.match(line).group('indent'))
            if indent_current == indent_parameter:
                # a new parameter has been encountered
                infos = re.split('[^\w]+', line.strip()) 
                parameter = infos[0]
                descriptions[parameter] = ['']
                if len(infos) == 2:
                    # the type has been defined so we save it
                    types[parameter] = infos[1]

            elif parameter:
                # in a parameter description: if 'parameter' is not set,
                # just skip the line!
                if line.strip():
                    # the line is not empty
                    buffer = self._handle_description(indent_current,
                                                      indent_description,
                                                      line,
                                                      descriptions[parameter])
                    descriptions[parameter] = buffer

                else:
                    # the line is empty
                    descriptions[parameter].append('\n')
                    descriptions[parameter].append('')
                 
        return [descriptions, types]


    def _handle_description(self, indent_current, indent_objective, line, buffer):
        buffer = buffer[:]
        if indent_current == indent_objective:
            # regular description line, so just add the content
            space = ' ' if buffer[-1] else ''
            buffer[-1] += space + line.strip()
        else:
            # not a regular description line, so put in its own string
            diff = indent_current - indent_objective
            space = ' ' * diff if diff > 0 else ''
            buffer.append(space + line.strip())
            buffer.append('')

        return buffer


    def make_prototype_class(self, node):
        base_classes = '(' + node.definition + ')' if node.definition else ''
        return node.indent * ' ' + 'class ' + node.name + base_classes + ':'


    def make_prototype_function(self, node):
        return node.indent * ' ' + 'def ' + node.name + '(' + node.definition + ')' + ':'


