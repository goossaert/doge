"""
Markup system.
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

from python_lang import PythonParser
from python_lang import PythonLang


from rst_reader import RestructuredTextReader
from rst_writer import RestructuredTextWriter


# Position fields
POSITION_BEFORE = 0
POSITION_AFTER = 1
POSITION_WITHIN = 2

# Stores markups
markups = {}

def declare_markup(id, markup):
    if id not in markups:
        markups[id] = markup


def find_markup(name, language):
    for id, markup in markups.items():
        if markup.name == name and markup.language == language:
            return markup 
    return None


class RSTPythonMarkup:

    multis = [('"""', '"""', POSITION_AFTER)] 

    singles = [('"""', '"""', POSITION_AFTER),
               ('#:', '', POSITION_AFTER and POSITION_WITHIN)
              ] 

    name = 'rst'
    language = 'python'
    extensions = ['.py']

    parser = PythonParser()
    lang = PythonLang()
    reader = RestructuredTextReader()
    writer = RestructuredTextWriter()


# Need to declare any available markup with a unique id and an object of that markup
declare_markup(RSTPythonMarkup.name + RSTPythonMarkup.language, RSTPythonMarkup())
