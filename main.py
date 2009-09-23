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

from file_parser import Parser
from writer import Writer
from python import PythonFactory

if __name__ == '__main__':
    parser = Parser()
    parser.read_file('file_parser.py')
    parser.print_file()
    parser.build_structure()
    pass
    writer = Writer()
    writer.write(parser.node_file)
    pass
    print ''.join(writer.buffer)

    ds = ['    truc\n',
          '        description\n',
          '        on multiple lines.',
          '    test : type\n',
          '                 \n',
          '    vide\n',
          '    bombe\n',
          '        interesring\n']

    factory = PythonFactory()
    factory.parse_sequence_parameter(None, ds)
