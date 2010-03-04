"""
Text module.
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


def format_text(text, indent, size):
    if text.startswith(' '):
        return ' ' * indent + text

    # get the position of all the spaces in the given text
    positions_space = [0] + [index + 1 for index, char in enumerate(text) if char == ' ']
    print positions_space
    print text

    positions_cut = []
    index_start = 0
    index_end = 0
    index_current = 0
    while index_current < len(positions_space):
        if positions_space[index_current] <= positions_space[index_start] + size - indent + 1:
            # The current space is still in the limit
            index_end = index_current
            index_current += 1
        else:
            # The current space has been found after the formatting limit
            # therefore a cut has to be done here
            positions_cut.append(positions_space[index_end])
            print '--- CUT FOUND:', positions_space[index_start], positions_space[index_end], positions_space[index_end] - positions_space[index_start]
            index_start = index_end
            index_current = index_start
    
    # Starting and ending positions are added, and sequence pairs are computed
    #positions_cut = [0] + positions_cut + [len(text)]
    positions_cut = [0] + positions_cut + [len(text)]
    limits = [(first, second) for first, second in zip(positions_cut[:-1], positions_cut[1:])]

    # The lines are constructed with valid indentation, jointed and returned
    newline = '\n' if text.endswith('\n') else ''
    print 'BEFORE format', text
    lines = [' ' * indent + text[limit[0]:limit[1]].rstrip() for limit in limits] 
    print 'AFTER format', lines
    return '\n'.join(lines) + newline


def is_one_liner(string):
    return True if '\n' not in string.rstrip() else False

