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
        print 'cleanup before:', text
        text = self._strip_first_empty_lines(text)
        text = [strip_newline(line) for line in text] # used to have a test: if line
        # replace empty line sequences by only one new line
        #text = [line for id, line in enumerate(text) if line and not id or text[id] or text[id - 1]]
        text = self._strip_last_empty_lines(text)
        # text is a list, so why do i have to do that? 
        #parameter.sd[0].text = text
        print 'cleanup after:', text

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
                section.sd[0].text = self._cleanup_text(section.sd[0].text) 

            


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
        docstring = self._strip_first_empty_lines(node.docstring[1:]) # omit the starting '"""'
        # find the cut between descriptions and sections and handle them
        id_cut = self._find_cut(docstring, lambda s: s.strip().startswith(':'))
        self._parse_docstring_descriptions(node, docstring[:id_cut])
        self._parse_docstring_sections(node, docstring[id_cut:])

    # TODO: as we always add a text to the section description, this text should be added automatically when building the SBSectionDescription instance!
    def _add_description(self, name, node, text, options=None):
        section = SBSectionDescription(node.padding, name, options)
        description = SBText(node.padding, text)
        section.sd.append(description)
        node.sf.sd.append(section)

        #indent_diff = node.indent_children - node.indent
        #indent_base = len(python_pattern.indent.match(docstring[0]).group('indent'))
        #padding = Padding(indent_base, indent_diff)


    def _parse_docstring_descriptions(self, node, docstring):
        # find the cut between short and long descriptions
        docstring = self._strip_lines(docstring)
        if docstring and not docstring[0].startswith('"""'):
            id_cut = self._find_cut(docstring, lambda s: not s.strip())
            print 'Short:', docstring[:id_cut]
            print 'Long:', docstring[id_cut+1:]
            self._add_description('*Short', node, docstring[:id_cut])
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
        sections_parameter = ['IVariables', 'CVariables', 'Variables', 'Parameters', 'Exceptions']
        in_description_short = True
        in_description_long = False

        for id_line, line_current in enumerate(docstring):

            # TODO for """, that should be endswith()
            # TODO treat cases where there is a starting """(text) and an ending (text)"""
            if any([line_current.strip().startswith(s) for s in ('@', ':', '"""')]):
                # section or end of docstring detected
                if section_current:
                    # already in a section, hence we have to treat it before
                    # setting up the new one
                    #sb_section = SBSection(node.padding, section_current, option_current)
                    print 'cur:', line_current
                    print 'prev:', line_previous
                    print '---'
                    if line_previous.strip().startswith('@'):
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
                    print 'options_current', options_current
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

        section = node.sf.find_section(title)
        if not section:
            section = SBSectionParameter(node.padding, title)
            node.sf.sd.append(section)
        parameter = SBParameter(node.padding, name)
        section.parameters[name] = parameter

        indent_diff = node.indent_children - node.indent
        indent_base = node.indent_children + indent_diff
        indent_description = indent_base + indent_diff
        padding = Padding(indent_base, indent_diff)

        first_line = [options[1].strip()] if options[1] else []
        buffer = ['']
        buffer = self._handle_description(indent_base,
                                          indent_description,
                                          first_line + docstring,
                                          buffer)
        description = SBText(padding, buffer)
        parameter.sd.append(description)


    def _handle_single_description(self, name, options, node, title, docstring):
        self._add_description(title, node, [options[1]] + docstring)
        print '++++++++ handle description'
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
                print '-- option parameters', len(options), options, name
                #section = node.sf.find_section(parameters[name])
                #print 'title', title
                self._handle_single_parameter(name, options, node, parameters[name], docstring)
        elif name in descriptions:
            print '-- option descriptions', len(options), options, name
            self._handle_single_description(name, options, node, descriptions[name], docstring)


    # TODO this function is never executed?
    def parse_section_text(self, name, options,  node, docstring):
        print 'parse_section_text', name, options, node, docstring
        #docstring = docstring[1:]
        #docstring = self._strip_lines(docstring)

        indent_diff = node.indent_children - node.indent
        indent_base = len(python_pattern.indent.match(docstring[0]).group('indent'))
        indent_description = indent_base# + indent_diff
        padding = Padding(indent_base, indent_diff)
        #print 'parse_section_text:', name, node.padding.base, node.padding.diff
        buffer = ['']
        for line in docstring:
            indent_current = len(python_pattern.indent.match(line).group('indent'))
            print 'current', 'description', line, indent_current, indent_description
            if indent_current == indent_description:
                buffer = self._handle_description(indent_current,
                                                  indent_description,
                                                  line,
                                                  buffer)


        #description = SBText(padding, buffer)
        #section = SBSectionDescription(node.padding, name, options)
        #print 'parse_section_text:', name, padding.base, padding.diff
        #section.sd.append(description)
        #node.sf.sd.append(section)
        print 'buffer', buffer
        self._add_description(name, node, buffer, options)



    def parse_section_parameter(self, name, options, node, docstring):
        if not docstring:
            return {}

        #docstring = docstring[1:]
        docstring = self._strip_first_empty_lines(docstring)


        indent_diff = node.indent_children - node.indent
        indent_base = node.indent_children
        indent_parameter = len(python_pattern.indent.match(docstring[0]).group('indent'))
        indent_description = indent_parameter + indent_diff
        padding = Padding(indent_parameter, indent_diff)

        section = SBSectionParameter(padding, name)
        #print 'parse_section_parameter', name, padding.base, padding.diff, 'i para', indent_parameter
        #print 'docstring', docstring
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
                    buffer = self._handle_description(indent_description,
                                                      indent_description,
                                                      infos[1],
                                                      buffer)
                else:
                    # definition list
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
                    buffer = self._handle_description(indent_current,
                                                      indent_description,
                                                      line,
                                                      buffer)
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


    # TODO rename
    def _handle_description(self, indent_current, indent_objective, lines, buffer):
        buffer = buffer[:]
        if not isinstance(lines, list):
            lines = [lines]

        for line in lines:
            indent_current = len(python_pattern.indent.match(line).group('indent'))
            print 'current', indent_current, 'obj', indent_objective, 'buffer', buffer
            if indent_current == indent_objective:
                # regular description line, so just add the content
                space = ' ' if buffer[-1] else ''
                buffer[-1] += space + line.strip()
            else:
                # not a regular description line, so put in its own string
                diff = indent_current - indent_objective
                print 'diff', diff
                space = ' ' * diff if diff > 0 else ''
                buffer.append(space + line.strip())
                #buffer.append('')

        return buffer

