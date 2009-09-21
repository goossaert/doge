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
        pass


    def parse_docstring_class(self, node):
        pass


    def parse_docstring_function(self, node):
        pass


    def parse_section(self, node, docstring):
        pass


    def parse_parameter_sequence(self, node, docstring):
        if not docstring:
            return {}

        pattern_indent = re.compile(
            r"""
            (?P<indent>[\s]*)
            .*?
            """, re.VERBOSE | re.DOTALL)


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
                    if indent_current == indent_description and line[indent_description] != ' ':
                        # regular description line, so just add the content
                        space = ' ' if descriptions[parameter][-1] else ''
                        descriptions[parameter][-1] += space + line.strip()
                    else:
                        # not a regular description line, so put in its own string
                        diff = indent_current - indent_description
                        space = ' ' * diff if diff > 0 else ''
                        descriptions[parameter].append(space + line.strip())
                        descriptions[parameter].append('')
                    
                else:
                    # the line is empty
                    descriptions[parameter].append('\n')
                    descriptions[parameter].append('')
                 
        print descriptions, types
        return descriptions, types


    def make_prototype_class(self, node):
        base_classes = '(' + node.definition + ')' if node.definition else ''
        return node.indent * ' ' + 'class ' + node.name + base_classes + ':'


    def make_prototype_function(self, node):
        return node.indent * ' ' + 'def ' + node.name + '(' + node.definition + ')' + ':'


