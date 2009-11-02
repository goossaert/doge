"""
Documentation class hierarchy.
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

from rst_writer import RestructuredTextWriter


# TODO delete the SB class hierarchy
class SB:
    def __init__(self, padding=None):
        self.padding = padding
        self.sd = []
        self.writer = RestructuredTextWriter()

    #def make_docstring(self):
    #    return ''.join(item.make_docstring() for item in self.sd)


    def find_section(self, name):
        for section in self.sd:
            #if (isinstance(section, SBSectionDescription) or isinstance(section, SBSectionParameter) ) and section.name == name:
            if isinstance(section, SBSection):
                if section.name == name:
                    return section
        return None


    def swallow(self, sb, sb_parent=None):
        for section_out in sb.sd:
            if isinstance(section_out, SBSection):
                section_in = self.find_section(section_out.name)
                if section_in:
                    section_in.swallow(section_out, sb)
                else:
                    self.sd.append(section_out)

    def make_docstring(self):
        print ''

            

class SBParameter(SB):
    def __init__(self, padding=None, name=None, type=None):
        SB.__init__(self, padding)
        self.name = name
        self.type = type

    def swallow(self, sb, sb_parent=None):
        self.name = sb.name
        self.type = sb.type



class SBText(SB):
    def __init__(self, padding=None, text=['']): # used to be []
        SB.__init__(self, padding)
        self.text = text

    def make_docstring(self):
        return self.writer.make_docstring_text_sb(self)

    def swallow(self, sb, sb_parent=None):
        self.text = sb.text



class SBSection(SB):
    def __init__(self, padding=None, name=None, option=None):
        SB.__init__(self, padding)
        self.name = name
        self.option = option



class SBSectionParameter(SBSection):
    def __init__(self, padding=None, name=None, option=None):
        SBSection.__init__(self, padding, name, option)
        self.parameters = {}

    def make_docstring(self):
        return self.writer.make_docstring_parameters_sb(self)

    def swallow(self, sb, sb_parent=None):
        self.parameters.update(sb.parameters) 

        section_types = sb_parent.find_section('Types')
        if section_types:
            self.swallow_types(section_types)

    def swallow_types(self, section_types):
        for name, parameter in section_types.parameters.items():
            if name in self.parameters:
                self.parameters[name].type = parameter.sd[0].text[0].strip()


class SBSectionDescription(SBSection):
    def __init__(self, padding=None, name=None, option=None):
        SBSection.__init__(self, padding, name, option)

    def make_docstring(self):
        return self.writer.make_docstring_description_sb(self)# + '\n'

    def swallow(self, sb, sb_parent=None):
        # TODO am i sure about that?
        self.sd = sb.sd
         


class SBBase(SB):
    def __init__(self, padding=None):
        SB.__init__(self, padding)

    def make_docstring(self):
        content = ''.join([item.make_docstring() for item in self.sd])
        return '--' + content + '--'
        #return self.writer.start(self.padding) + content + self.writer.end(self.padding)


class SBFile(SBBase):
    def __init__(self, padding=None):
        SBBase.__init__(self, padding)


    def make_docstring(self):
        content = self.writer.make_docstring_file(self)
        return self.writer.start(self.padding, content) + content + self.writer.end(self.padding)


class SBClass(SBBase):
    def __init__(self, padding=None):
        SBBase.__init__(self, padding)


    def make_docstring(self):
        content = self.writer.make_docstring_class(self)
        return self.writer.start(self.padding, content) + content + self.writer.end(self.padding, content)



class SBFunction(SBBase):
    def __init__(self, padding=None):
        SBBase.__init__(self, padding)


    def make_docstring(self):
        content = self.writer.make_docstring_function(self)
        return self.writer.start(self.padding, content) + content + self.writer.end(self.padding, content)
