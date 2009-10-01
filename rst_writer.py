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
import doc

#from doc import SBSection


pattern_indent = re.compile(
    r"""
    (?P<indent>[\s]*)
    .*?
    """, re.VERBOSE | re.DOTALL)


pattern_section = re.compile(
    r"""
    (?P<indent>[\s]*)
    [:]
    (?P<title>[\w]*)
    ([\s]*(?P<option>[\w]*))?
    [:]
    .*?
    """, re.VERBOSE | re.DOTALL)




class RestructuredTextWriter:

    def __init__(self):
        pass

    def make_docstring(self, node):
        for section in node.sf:
            pass


    def start(self, padding):
        return padding.padding(0) + '"""\n'
              

    def end(self, padding):
        return self.start(padding)


    def make_docstring_file(self, node):
        return ''


    def make_docstring_list(self, sb, list):
        #print 'make_docstring_list'
        docstring = []
        #list = list[:] # local copy
        for name in list:
            # TODO replace the list in SB by a dictionary: for SB with no name,
            # take the len of the dict at the moment of the add
            
            for section in sb.sd:
                name_section = getattr(section, 'name', None)
                if name_section and name_section == name:
                    #print 'doc_list:', section, name
                    docstring.append(section.make_docstring())

        return '\n'.join(docstring)



    def make_docstring_not_list(self, sb, list):
        docstring = []
        for section in sb.sd:
            for name in list:
                name_section = getattr(section, 'name', None)
                if not name_section or name_section != name:
                    #docstring.append(section.make_docstring(name_section))
                    docstring.append(section.make_docstring())
                    

                    
                   
        return '\n'.join(docstring)



    def make_docstring_class(self, sb):
                    #self.buffer.append(self.rst.start(node.padding))
                    #self.buffer.append(self.rst.end(node.padding))
        #if not doc.find_section('CVariables', node.sf) and not doc.find_section('IVariables', node.sf):
        #    return ''

        list = ['Short', 'Long', 'IVariables', 'CVariables']
        print 'make docstring class'

        priority = self.make_docstring_list(sb, list)
        non_priority = self.make_docstring_not_list(sb, list)

        print 'writer class'

        return priority
        #return priority + non_priority








        pass

        doc_variable = '%s%s\n\
                        %s%s\n'.replace(' ','')

        doc_section = '\n\
                        %(indent)s:%(section)s:\n\
                        %(variables)s'.replace(' ','')

        doc_function = '%(indent)s\n\
                        %(indent)s%(description)s%(content)s\
                        %(indent)s\n'.replace(' ', '')

        # TODO factorize with make_docstring for functions
        diff = node.indent_children - node.indent
        #indent_name = ' ' * (node.indent_children + diff)
        #indent_description = ' ' * (node.indent_children + diff * 2)
        #indent = ' ' * node.indent_children

        #var_class = [doc_variable % (indent_name, name, indent_description, ''.join(description)) for name, description in node.variables_class.items()]
        var_class = []
        var_class_content = doc_section % {'indent': indent,
                                           'section': 'CVariables',
                                           'variables': ''.join(var_class)}

        #var_instance = [doc_variable % (indent_name, name, indent_description, ''.join(description)) for name, description in node.variables_instance.items()]
        var_instance = []
        var_instance_content = doc_section % {'indent': indent,
                                              'section': 'IVariables',
                                              'variables': ''.join(var_instance)}

        content = ''
        if var_class:
            content += var_class_content

        if var_instance:
            content += var_instance_content

        return doc_function % {'indent': indent,
                               #'description': ''.join(node.descriptions[0] + ['\n'] + node.descriptions[1]),
                               'description': '',
                               'content': content}


    def _cut_line(self, line, len_editable):
        words = re.split('\s', line)
        id_cut = 0
        if len(words[0]) >= len_editable:
            # first word bigger than the line: can't cut it!
            id_cut = 1
        else :
            # else, let's decompose the line
            len_cut = 0
            while len_cut < len_editable:
                id_cut += 1
                len_cut = len(' '.join(words[:id_cut]))
            id_cut -= 1

        return words[:id_cut], words[id_cut:] 


    def _format_lines(self, lines, len_indent, len_max=80):
        formatted = []
        len_editable = len_max - len_indent
        if len_editable <= 0:
            return lines
        
        for line in lines:
            indexes = [(pos * len_editable, (pos + 1) * len_editable) for pos in range((len(lines) // len_editable) + 1)]
            for index in indexes:
                start = index(0)
                end = index(1)
                formatted.append(' ' * len_indent + line[start, end])
                

    def _make_docstring_description(self, node):
        doc_description = '%s%s\n'.replace(' ','')
        description_short = [doc_description % (indent, line) for line in node.descriptions[0]]
        description_long = [doc_description % (indent, line) for line in node.descriptions[1]]


    def _make_docstring_parameters(self, node, parameters):
        doc_parameter = '%s%s\n\
                         %s%s\n'.replace(' ','')
        return [doc_parameter % (indent_name, name, indent_description, ''.join(description)) for name, description in parameters.items()]


    def make_docstring_function(self, sb):
        list = ['Short', 'Long', 'Parameters']

        priority = self.make_docstring_list(sb, list)
        non_priority = self.make_docstring_not_list(sb, list)

        return priority
        #return priority + non_priority





        if not node.sf.find_section('Parameters'):
            return ''
        return ''

        doc_function = '%(indent)s\n\
                        %(description_short)s\
                        %(description_long)s\
                        %(indent)s:Parameters:\n\
                        %(parameters)s\
                        %(indent)s\n'.replace(' ','')

        indent_diff = node.indent_children - node.indent
        #indent_name = ' ' * (node.indent_children + indent_diff)
        #indent_description = ' ' * (node.indent_children + indent_diff * 2)
        #indent = ' ' * node.indent_children

        parameters = self._make_docstring_parameters(indent_name, {})#node.parameters)

        return doc_function % {'indent': indent,
                               #'description': ''.join(node.descriptions[0] + ['\n'] + node.descriptions[1]),
                               'description_short': '',
                               'description_long': '',
                               'parameters': ''.join(parameters)}


    def make_prototype_class(self, node):
        base_classes = '(' + node.definition + ')' if node.definition else ''
        return node.indent * ' ' + 'class ' + node.name + base_classes + ':'


    def make_prototype_function(self, node):
        return node.indent * ' ' + 'def ' + node.name + '(' + node.definition + ')' + ':'


    def make_docstring_text_sb(self, section, level_indent):
        #print 'ds text:', section
        return section.padding.padding(level_indent) + ''.join(section.text)


    def make_docstring_description_sb(self, section):
        #print 'ds description:', section
        return ''.join(self.make_docstring_text_sb(s, level_indent=0) for s in section.sd)

    
    def make_docstring_parameters_sb(self, sb):
        doc_parameter = '%s%s\n\
                         %s%s\n'.replace(' ','')
        buffer = [sb.padding.padding(0) + ':' + sb.name +':\n']
        for parameter in sb.parameters.values():
            name = parameter.name
            type = parameter.type

            text = ''.join([self.make_docstring_text_sb(s, level_indent=2) for s in parameter.sd])
            doc_title = '%(indent)s%(name)s : %(type)s' if type else '%(indent)s%(name)s'
            title = doc_title % {'name': name, 'type': type, 'indent': sb.padding.padding(1)}
            docstring = doc_parameter % ('', title, '', text)
            buffer.append(docstring)
        return ''.join(buffer)

        #return [doc_parameter % (indent_name, name, indent_description, ''.join(description)) for name, description in section.parameters.items()]
