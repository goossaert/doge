"""
Utility module 0.1
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




def flatten(obj):
    """Return all the objects contained in an iterable object."""
    if issequence(obj):
        # TODO check if we can loop on sets
        for o in obj:
            for o_flat in flatten(o):
                yield o_flat
    else:
        yield obj
   

def issequence(obj):
    # TODO check on what is a sequence
    return isinstance(obj, (list, tuple, dict, set))


def isiterable(obj):
    return isinstance(obj, basestring) or issequence(obj)


def all_true(obj):
    """
    Return a list with all the non-None, non-empty or non-False objects contained
    in the passed object.
    """
    return [e for e in obj if e]
    

def make_list(obj):
    """Make a directly iterable list from an object or a recursive list."""
    if not issequence(obj):
        obj_valid = [obj]
    else:
        # if obj is just one element into subsequences, then we just unpack it
        obj_valid = list(obj)[:]
        while isinstance(obj_valid, list) and len(obj_valid) == 1 and isinstance(obj_valid[0], list):
            obj_valid = obj_valid[0]

    return obj_valid

