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
import python_pattern

from padding import Padding
from doc import *


class RestructuredTextReader: 
    def __init__(self):
        pass


    def _cleanup_parameters(self, parameters):
        for name, parameter in parameters.items():
            parameter.sd[0].text = self._cleanup_text(parameter.sd[0].text)

    def _cleanup_text(self, text):
        strip_newline = lambda string: '' if string == '\n' else string
        #text = parameter.sd[0].text
        # replace new lines by empty lines
        text = self._strip_first_empty_lines(text)
        text = [strip_newline(line) for line in text] # used to have a test: if line
        # replace empty line sequences by only one new line
        #text = [line for id, line in enumerate(text) if line and not id or text[id] or text[id - 1]]
        text = self._strip_last_empty_lines(text)
        # text is a list, so why do i have to do that? 
        #parameter.sd[0].text = text

        return text


    def _cleanup_section(self, node, name):
        section = node.sf.find_section(name)
        if section:
              self._cleanup_parameters(section.parameters)

    def _cleanup_sections(self, node):
        for section in node.sf.sd:
            if isinstance(section, SBSectionParameter):
                self._cleanup_parameters(section.parameters) 
            elif isinstance(section, SBSectionDescription):
                #print 'BEFORE cleanup:', section.sd[0].text
                section.sd[0].text = self._cleanup_text(section.sd[0].text) 
                #print 'AFTER cleanup:', section.sd[0].text

    def merge_types_section(self, node):
        # the type section has to be merged to the parameter one
        pass
            


    #def _fill_descriptions(self, node, descriptions):
    #    node.descriptions = descriptions


    #def _fill_parameters(self, titles, sections):
    #    for title in titles:
    #        (name, parameters, types) = title
    #        if name in sections:
    #            parameters.update(sections[name][0]) 
    #            types.update(sections[name][1])
    #            self._cleanup_parameters(parameters)
    #            self._cleanup_parameters(types)



    def parse_docstring_file(self, node):
        self.parse_docstring(node)
        self._cleanup_sections(node)
        #self._cleanup_section(node, 'Parameters')


    def parse_docstring_class(self, node):
        self.parse_docstring(node)
        self._cleanup_sections(node)
        #self._cleanup_section(node, 'CVariables')
        #self._cleanup_section(node, 'IVariables')


    def parse_docstring_function(self, node):
        self.parse_docstring(node)
        self._cleanup_sections(node)
        #self._cleanup_section(node, 'Parameters')
        #self._cleanup_section(node, 'Exceptions')


    def _find_cut(self, docstring, fct_string):
        for id_line, line in enumerate(docstring):
            if fct_string(line):
                return id_line
        return len(docstring)


    def parse_docstring(self, node):
        seq_start = '"""'
        seq_end = '"""'
        #print node.docstring[0].strip()
        # omit the starting '"""'
        # TODO: modify to handle multiple start sequences
        line_first = [node.docstring[0].strip()[len(seq_start):]] if node.docstring else []
        if node.docstring:
            print line_first, node.docstring
        docstring = self._strip_first_empty_lines(line_first + node.docstring[1:])
        # move the ending """
        if docstring:
            docstring[-1] = docstring[-1].rstrip()[:-len(seq_end)]
            docstring.append(seq_end)
            #else:
            #    pass
            #    print 'handle description ELSE', '|' + docstring[0][:-len(seq_end)] + '|'
            #    self._add_description('*Short', node, [docstring[0].strip()[:-len(seq_end)]])
        # find the cut between descriptions and sections and handle them
        id_cut = self._find_cut(docstring, lambda s: s.strip().startswith(':'))
        #print 'after strip', docstring
        self._parse_docstring_descriptions(node, docstring[:id_cut])
        self._parse_docstring_sections(node, docstring[id_cut:])

    # TODO: as we always add a text to the section description, this text should be added automatically when building the SBSectionDescription instance!
    def _add_description(self, name, node, text, padding=None, options=None):
        if padding == None:
            padding = node.padding
        section = SBSectionDescription(padding, name, options)
        description = SBText(node.padding, text)
        section.sd.append(description)
        node.sf.sd.append(section)

        #indent_diff = node.indent_children - node.indent
        #indent_base = len(python_pattern.indent.match(docstring[0]).group('indent'))
        #padding = Padding(indent_base, indent_diff)


    def _parse_docstring_descriptions(self, node, docstring):
        # find the cut between short and long descriptions
        seq_end = '"""'
        #docstring = self._strip_lines(docstring)
        # TODO: modify to handle multiple end sequences
        if docstring:# and not docstring[0].rstrip().endswith(seq_end):
            if docstring[-1].rstrip().endswith(seq_end):
                docstring = docstring[:-1]
            id_cut = self._find_cut(docstring, lambda s: not s.strip())
            print 'handle description', docstring[:id_cut], '|||', docstring[id_cut+1:]
            self._add_description('*Short', node, docstring[:id_cut])
            if docstring[id_cut+1:]:
                self._add_description('*Long', node, docstring[id_cut+1:])


    # TODO modify the function so that it first split the docstring
    # into sections, and then treat them?
    def _parse_docstring_sections(self, node, docstring):
        docstring = self._strip_first_empty_lines(node.docstring[1:]) # omit the starting '"""'
        id_section = None
        line_previous = ''
        options_current = None
        options_previous = None
        section_current = None
        section_previous = None
        #sections_text = ['Return', 'Raises']
        sections_parameter = ['IVariables', 'CVariables', 'Variables', 'Parameters', 'Exceptions', 'Types']
        in_description_short = True
        in_description_long = False

        for id_line, line_current in enumerate(docstring):

            # TODO for """, that should be endswith()
            # TODO treat cases where there is a starting """(text) and an ending (text)"""
            #   and for that, maybe exclude the content of the if one more time for """
            #   or pre-treat the docstring and put on separate line the """
            if any([line_current.lstrip().startswith(s) for s in ('@', ':')]) \
              or any([line_current.rstrip().endswith(s) for s in ('"""')]):
                # section or end of docstring detected
                if section_current:
                    # already in a section, hence we have to treat it before
                    # setting up the new one
                    #sb_section = SBSection(node.padding, section_current, option_current)
                    if line_previous.lstrip().startswith('@'):
                        parser = self.parse_section_single
                    elif section_previous in sections_parameter: 
                        parser = self.parse_section_parameter 
                    else:
                        parser = self.parse_section_text

                    parser(section_previous,
                           options_previous,
                           node,
                           docstring[id_section + 1:id_line])
                    #node.sf.append(sb_section)
                     
                match = python_pattern.section.match(line_current)
                if match:
                    section_current = match.group('title')
                    options_current = [match.group('option'), match.group('content')]
                id_section = id_line

                line_previous = line_current
                section_previous = section_current
                options_previous = options_current


    def _strip_lines(self, lines):
        return [line.strip() for line in lines]

    def _strip_last_empty_lines(self, lines):
        while lines and not lines[-1].strip():
            lines = lines[:-1]
        return lines

    def _strip_first_empty_lines(self, lines):
        # skip the empty lines at the beginning of the docstring
        while lines and not lines[0].strip():
            lines = lines[1:]
        return lines
        #id_start = None
        #for id_line, line in enumerate(lines):
        #    if not line.strip():
        #        id_start = id_line + 1
        #    else:
        #        break
        #return lines[id_start:]


    # TODO from python_lang.py: delete?
    def _handle_single_parameter(self, name, options, node, title, docstring):
        if not name:
            return

        indent_diff = node.indent_children - node.indent
        indent_base = node.indent_children # TODO: should be indent_children?
        indent_parameter = indent_base + indent_diff # TODO: should be indent_children?
        indent_description = indent_parameter + indent_diff
        padding = Padding(indent_base, indent_diff)
        print 'indent', indent_base, indent_parameter, indent_description
        #indent_parameter = len(python_pattern.indent.match(docstring[0]).group('indent'))

        section = node.sf.find_section(title)
        if not section:
            section = SBSectionParameter(padding, title) # used to be node.padding
            node.sf.sd.append(section)
        parameter = SBParameter(padding, options[0]) # used to be node.padding
        section.parameters[options[0]] = parameter

        first_line = [options[1].strip()] if options[1] else []
        #buffer = ['']
        #buffer = self._handle_description(indent_parameter,
        #                                  indent_description,
        #                                  first_line + docstring,
        #                                  buffer)
        #print 'single', first_line, docstring, first_line + docstring, buffer
        # description = SBText(padding, buffer) with use of handle description
        description = SBText(padding, first_line + docstring)
        parameter.sd.append(description)


    def _handle_single_description(self, name, options, node, title, docstring):
        self._add_description(title, node, [options[1]] + docstring)
        return

        indent_diff = node.indent_children - node.indent
        indent_base = node.indent_children + indent_diff
        indent_description = indent_base + indent_diff
        padding = Padding(indent_base, indent_diff)


        #description = SBText(padding, buffer)
        #section = SBSectionDescription(node.padding, name, options)
        #print 'parse_section_text:', name, padding.base, padding.diff
        #section.sd.append(description)
        #node.sf.sd.append(section)
        self._add_description(name, node, buffer, options)


    def parse_section_single(self, name, options, node, docstring):
        #indent_diff = node.indent_children - node.indent
        #indent_base = len(python_pattern.indent.match(docstring[0]).group('indent'))# + indent_diff
        #padding = Padding(indent_base, indent_diff)

        # get the description text, and then decide on what to do based on the name.

        parameters = {# Functions and Methods
                      'param':          'Parameters',
                      'parameter':      'Parameters',
                      'arg':            'Parameters',
                      'argument':       'Parameters',
                      'type':           'Types',
                      'keyword':        'Keywords',
                      'kwarg':          'Keywords',
                      'kwparams':       'Keywords',
                      'raise':          'Exceptions',
                      'raises':         'Exceptions',
                      'except':         'Exceptions',
                      'exception':      'Exceptions',

                      # Variables
                      'ivar':           'IVariables',
                      'ivariables':     'IVariables',
                      'cvar':           'CVariables',
                      'cvariables':     'CVariables',
                      'var':            'Variables',
                      'variable':       'Variables',

                      # Grouping and Sorting
                      'group':          'Groups',

                      # Status
                      'todo':           'Todos'}

        descriptions = {# Functions and Methods
                        'type':             'Type',
                        'return':           'Return',
                        'returns':          'Return',
                        'rtype':            'ReturnType',
                        'returntype':       'ReturnType',

                        # Grouping and Sorting
                        'sort':             'Sort',

                        # Related Topics
                        'see':              'SeeAlso',
                        'seealso':          'SeeAlso',

                        # Notes and Warnings 
                        'node':             'Note',
                        'attention':        'Attention',
                        'bug':              'Bug',
                        'warning':          'Warning',
                        'warn':             'Warning',

                        # Formal Conditions 
                        'requires':       'Requires',
                        'require':        'Requires',
                        'requirements':   'Requires',
                        'precondition':   'PreCondition',
                        'precond':        'PreCondition',
                        'postcondition':  'PostCondition',
                        'postcond':       'PostCondition',
                        'invariant':      'Invariant',

                        # Bibliographic Information
                        'author':         'Author',
                        'organization':   'Organization',
                        'org':            'Organization',
                        'copyright':      'Copyright',
                        '(c)':            'Copyright',
                        'license':        'License',
                        'contact':        'Contact',
                        
                        # Summarization 
                        'summary':        'Summary',

                        # Status
                        'version':        'Version',
                        'deprecated':     'Deprecated',
                        'since':          'Since',
                        'status':         'Status',
                        'change':         'Change',
                        'changed':        'Change',
                        'permission':     'Permission',
                }

        if options[0]:
            # it has a argument, so it is a parameter
            if name in parameters:
                #section = node.sf.find_section(parameters[name])
                #print 'title', title
                self._handle_single_parameter(name, options, node, parameters[name], docstring)
        elif name in descriptions:
            self._handle_single_description(name, options, node, descriptions[name], docstring)


    # TODO this function is never executed?
    def parse_section_text(self, name, options,  node, docstring):
        #docstring = docstring[1:]
        #docstring = self._strip_lines(docstring)

        indent_diff = node.indent_children - node.indent
        indent_base = node.indent_children
        #indent_description = indent_base + indent_diff
        indent_description = len(python_pattern.indent.match(docstring[0]).group('indent'))
        padding = Padding(indent_base, indent_diff)
        buffer = ['']
        #for line in docstring:
        #    indent_current = len(python_pattern.indent.match(line).group('indent'))
        #    if indent_current >= indent_description:
        #        buffer = self._handle_description(indent_current,
        #                                          indent_description,
        #                                          line,
        #                                          buffer)


        #description = SBText(padding, buffer)
        #section = SBSectionDescription(node.padding, name, options)
        #print 'parse_section_text:', name, padding.base, padding.diff
        #section.sd.append(description)
        #node.sf.sd.append(section)
        self._add_description(name, node, docstring, padding, options)
        #self._add_description(name, node, buffer, padding, options)



    def parse_section_parameter(self, name, options, node, docstring):
        if not docstring:
            return {}

        #docstring = docstring[1:]
        docstring = self._strip_first_empty_lines(docstring)

        indent_diff = node.indent_children - node.indent
        indent_base = node.indent_children
        indent_parameter = indent_base + indent_diff # TODO: should be indent_children?
        #indent_parameter = len(python_pattern.indent.match(docstring[0]).group('indent'))
        indent_description = indent_parameter + indent_diff
        padding = Padding(indent_base, indent_diff)

        section = SBSectionParameter(padding, name)
        node.sf.sd.append(section)

        parameter = None
        buffer = ['']
        for line in docstring:
            indent_current = len(python_pattern.indent.match(line).group('indent'))
            if indent_current == indent_parameter:
                # a new parameter has been encountered

                if parameter:
                    # if a parameter was being addressed, it has to be saved
                    description = SBText(padding, buffer)
                    parameter.sd.append(description)
                    #print 'param', parameter, description, buffer
                    buffer = ['']

                if line.strip().startswith('-'):
                    # bulleted list
                    infos = re.split('[\s\-:]+', line.strip(), 2) 
                    infos = [item for item in infos if item]
                    name = infos[0][1:-1] # skip the '`' that surround the name
                    type = ''
                    #buffer = self._handle_description(indent_current,
                    #                                  indent_description,
                    #                                  infos[1],
                    #                                  buffer)
                    buffer += [infos[1]]
                else:
                    # parsing definition lists
                    infos = re.split('[\s\-:]+', line.strip(), 1) 
                    name = infos[0]
                    type = infos[1] if len(infos) > 1 else ''
                section.parameters[name] = SBParameter(padding, name, type)
                parameter = section.parameters[name]

            elif parameter:
                # in a parameter description: if 'parameter' is not set,
                # just skip the line!
                if line.strip():
                    # the line is not empty
                    #buffer = self._handle_description(indent_current,
                    #                                  indent_description,
                    #                                  line,
                    #                                  buffer)
                    buffer += [line]
                else:
                    # the line is empty
                    buffer.append('\n')
                    buffer.append('')

        # in case the parameter is at the end of the list, but maybe recode this in a cleaner way
        if parameter:
            # if a parameter was being addressed, it has to be saved
            description = SBText(padding, buffer)
            parameter.sd.append(description)
            #print 'param', parameter, description, buffer


    #TODO: delete     #previous TODO: rename
    def _handle_description(self, indent_current, indent_objective, lines, buffer):
        buffer = buffer[:]
        # TODO replace with make_list()
        if not isinstance(lines, list):
            lines = [lines]

        for line in lines:
            #indent_current = len(python_pattern.indent.match(line).group('indent'))
            if indent_current <= indent_objective:
                #regular description line, so just add the content
                space = ' ' if buffer[-1] else ''
                buffer[-1] += space + line.strip()
            else:
            #if True:
                # not a regular description line, so put in its own string
                diff = indent_current - indent_objective
                space = ' ' * diff if diff > 0 else ''
                buffer.append(space + line.strip())
                buffer.append('')

        return buffer

