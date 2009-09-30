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


    def swallow(self, sb):
        for section_out in sb.sd:
            if isinstance(section_out, SBSection):
                section_in = self.find_section(section_out.name)
                if section_in:
                    section_in.swallow(section_out)
                else:
                    print 'add:', section_out.name
                    self.sd.append(section_out)


            

class SBParameter(SB):
    def __init__(self, padding=None, name=None, type=None):
        SB.__init__(self, padding)
        self.name = name
        self.type = type

    def swallow(self, sb):
        self.name = sb.name
        self.type = sb.type



class SBText(SB):
    def __init__(self, padding=None, text=[]):
        SB.__init__(self, padding)
        self.text = text

    def make_docstring(self):
        return self.writer.make_docstring_text_sb(self)

    def swallow(self, sb):
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

    def swallow(self, sb):
        self.parameters.update(sb.parameters) 



class SBSectionDescription(SBSection):
    def __init__(self, padding=None, name=None, option=None):
        SBSection.__init__(self, padding, name, option)

    def make_docstring(self):
        return self.writer.make_docstring_description_sb(self)

    def swallow(self, sb):
        # TODO am i sure about that?
        self.sd = sb.sd
         


class SBBase(SB):
    def __init__(self, padding=None):
        SB.__init__(self, padding)

    def make_docstring(self):
        content = ''.join([item.make_docstring() for item in self.sd])
        return self.writer.start(self.padding) + content + self.writer.end(self.padding)



class SBFile(SBBase):
    def __init__(self, padding=None):
        SBBase.__init__(self, padding)



class SBClass(SBBase):
    def __init__(self, padding=None):
        SBBase.__init__(self, padding)



class SBFunction(SBBase):
    def __init__(self, padding=None):
        SBBase.__init__(self, padding)

