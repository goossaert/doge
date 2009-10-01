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

from padding import Padding
from doc import *


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


class RestructuredTextReader: 
    def __init__(self):
        pass


    def _cleanup_parameters(self, parameters):
        strip_newline = lambda string: '' if string == '\n' else string + '\n'

        for name, descriptions in parameters.items():
            parameters[name] = [strip_newline(d) for d in descriptions if d]


    def _fill_descriptions(self, node, descriptions):
        node.descriptions = descriptions


    def _fill_parameters(self, titles, sections):
        for title in titles:
            (name, parameters, types) = title
            if name in sections:
                parameters.update(sections[name][0]) 
                types.update(sections[name][1])
                self._cleanup_parameters(parameters)
                self._cleanup_parameters(types)


    def parse_docstring_file(self, node):
        self.parse_docstring(node)
        return
        titles = [('Parameters', node.parameters, node.types)]
        self._fill_descriptions(node, descriptions)
        self._fill_parameters(titles, sections)


    def parse_docstring_class(self, node):
        self.parse_docstring(node)
        return
        titles = [('CVariables', node.variables_class, node.types_class),
                  ('IVariables', node.variables_instance, node.types_instance)]
        self._fill_descriptions(node, descriptions)
        self._fill_parameters(titles, sections)


    def parse_docstring_function(self, node):
        self.parse_docstring(node)
        return
        titles = [('Parameters', node.parameters, node.types)]
        self._fill_descriptions(node, descriptions)
        self._fill_parameters(titles, sections)


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


    def _add_description(self, name, node, text):
        pass
        section = SBSectionDescription(node.padding, name)
        print '_add_description:', name, node.padding.base, node.padding.diff
        description = SBText(node.padding, text)
        section.sd.append(description)
        node.sf.sd.append(section)

        #indent_diff = node.indent_children - node.indent
        #indent_base = len(pattern_indent.match(docstring[0]).group('indent'))
        #padding = Padding(indent_base, indent_diff)


    def _parse_docstring_descriptions(self, node, docstring):
        # find the cut between short and long descriptions
        docstring = self._strip_lines(docstring)
        if docstring and not docstring[0].startswith('"""'):
            id_cut = self._find_cut(docstring, lambda s: not s.strip())
            self._add_description('Short', node, docstring[:id_cut])
            self._add_description('Long', node, docstring[id_cut+1:])


    # TODO modify the function so that it first split the docstring
    # into sections, and then treat them?
    def _parse_docstring_sections(self, node, docstring):
        docstring = self._strip_first_empty_lines(node.docstring[1:]) # omit the starting '"""'
        id_section = None
        options_current = None
        section_current = None
        sections_text = ['Returns', 'Raises']
        sections_parameter = ['IVariables', 'CVariables', 'Parameters']
        in_description_short = True
        in_description_long = False

        for id_line, line in enumerate(docstring):

            # look for sections or end of docstring
            if line.strip().startswith(':') or line.strip().startswith('"""'):
                # section, or end of docstring detected
                if section_current:
                    # already in a section, hence we have to treat it before
                    # setting up the new one
                    #sb_section = SBSection(node.padding, section_current, option_current)
                    parser = self.parse_section_parameter if section_current in sections_parameter else self.parse_section_text
                    parser(section_current,
                           options_current,
                           node,
                           docstring[id_section + 1:id_line])
                    #node.sf.append(sb_section)
                     
                match = pattern_section.match(line)
                if match:
                    section_current = match.group('title')
                    options_current = match.group('option')
                id_section = id_line


    def _strip_lines(self, lines):
        return [line.strip() for line in lines]


    def _strip_first_empty_lines(self, lines):
        # skip the empty lines at the beginning of the docstring
        id_start = None
        for id_line, line in enumerate(lines):
            if not line.strip():
                id_start = id_line + 1
            else:
                break
        return lines[id_start:]


    def parse_section_text(self, name, options, node, docstring):
        docstring = self._strip_docstring(docstring)

        indent_diff = node.indent_children - node.indent
        indent_base = len(pattern_indent.match(docstring[0]).group('indent'))
        padding = Padding(indent_base, indent_diff)
        print 'parse_section_text:', name, node.padding.base, node.padding.diff
        buffer = ['']
        for line in docstring:
            indent_current = len(pattern_indent.match(line).group('indent'))
            if indent_current == indent_description:
                buffer = self._handle_description(indent_current,
                                                  indent_description,
                                                  line,
                                                  buffer)

        description = SBText(padding, buffer)
        section = SBSectionDescription(node.padding, name, options)
        print 'parse_section_text:', name, padding.base, padding.diff
        section.sd.append(description)
        node.sf.sd.append(section)


    def parse_section_parameter(self, name, options, node, docstring):
        if not docstring:
            return {}

        docstring = self._strip_first_empty_lines(docstring)


        #indent_diff = node.indent_children - node.indent
        #indent_diff = 4
        #indent_description = indent_parameter + indent_diff 
        indent_diff = node.indent_children - node.indent
        indent_base = node.indent_children
        #indent_base = len(pattern_indent.match(docstring[0]).group('indent'))
        indent_parameter = len(pattern_indent.match(docstring[0]).group('indent')) + indent_diff
        indent_description = indent_parameter
        padding = Padding(indent_base, indent_diff)

        section = SBSectionParameter(padding, name)
        print 'parse_section_parameter', name, padding.base, padding.diff
        node.sf.sd.append(section)

        parameter = None
        buffer = ['']
        for line in docstring:
            indent_current = len(pattern_indent.match(line).group('indent'))
            if indent_current == indent_parameter:
                # a new parameter has been encountered
                if parameter:
                    # if a parameter was being addressed, it has to be saved
                    description = SBText(padding, buffer)
                    parameter.sd.append(description)
                    buffer = ['']
                infos = re.split('[^\w]+', line.strip()) 
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


    # TODO rename
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



