"""
Filesystem functions.
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

import os
import sys
import logging

logger = logging.getLogger(os.path.basename(sys.argv[0]))


# TODO from gage, code for files and directories
def get_directories(directories, recursive=False):
    #self.path_directory_output = None
    #paths_directory_input = []
    #for rule_directory in self.rule_set.get_rules_by_type('RuleDirectoryPermission'):
    #    if rule_directory.action == 'input':
    #        paths_directory_input.append(os.path.join(name_directory_base, rule_directory.name_directory))
        #elif not self.path_directory_output: # action == 'output'
        #    pass

    #if not self.path_directory_output:
    #    self.path_directory_output = self.path_directory_output_default
    #    logger.warning('No output directory given, using default: "%s"' % self.path_directory_output)

    directories_output = []
    while directories:
        directory = directories.pop()
        if os.path.exists(directory):
            # Save the popped directory
            directories_output.append(directory)
            logger.info('Handling directory: "%s"' % directory)
            if recursive:
                inodes_all = [os.path.join(directory, f) for f in os.listdir(directory)]
                directories_all = [d for d in inodes_all if os.path.isdir(d)]
                # Add the new directories for the current loop,
                directories.extend(directories_all)
        else:
            logger.error('Error path: the directory "%s" does not exists!' % path_directory)

    return directories_output


def get_files(directories, extensions):
    files_output = []
    for directory in directories:
        inodes_all = [os.path.join(directory, f) for f in os.listdir(directory)]
        files_all = [f for f in inodes_all if os.path.isfile(f) and os.path.splitext(f)[1] in extensions]
        files_output.extend(files_all)

    for file in files_output:
        logger.info('Handling file: "%s"' % file)

    return files_output


# TODO add exception check in this function
def copy_dir_hierarchy(files, dir_source, dir_dest, mode=0755):
    # get all directory names from file paths
    dirs_all = [os.path.dirname(file) for file in files]
    # sort the paths and make sure they are unique
    dirs_sorted = sorted(list(set(dirs_all)))
    # delete directories that are part of other hierarchies
    filter = lambda index: index == len(dirs_sorted) - 1 or not dirs_sorted[index + 1].startswith(dirs_sorted[index])
    dirs_filtered = [dir for index, dir in enumerate(dirs_sorted) if filter(index)] 
    # replace directory prefix
    dirs = [os.path.join(dir_dest, d[len(dir_source):]) for d in dirs_filtered] 

    for dir in dirs:
        try:                os.makedirs(dir, mode)
        except OSError, e:  pass 


def transform_filepath(filepath, dir_source, dir_dest):
    return os.path.join(dir_dest, filepath[len(dir_source):])


# TODO function to copy directory hierarchy
# TODO function to transform a file path into a destionation path
