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

import os
import sys
import logging
import ut
from optparse import OptionParser

import markup
from python_lang import PythonParser
from python_lang import PythonLang
from writer import Writer
from rst_reader import RestructuredTextReader
from rst_writer import RestructuredTextWriter
from node import Node


logger = logging.getLogger(os.path.basename(sys.argv[0]))



def configure_logging(level=logging.DEBUG):
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')


def set_logger(options):
    if options.verbose:
        level_logging = logging.INFO
    elif options.quiet:
        level_logging = logging.CRITICAL
    elif options.debug:
        level_logging = logging.DEBUG
    else:
        level_logging = logging.WARNING
    configure_logging(level_logging) 


def set_option_parser(parser):
    path_directory_output_default = 'documented'
    parser.add_option('-m', '--input-markup', action='store', type='string', dest='markup_input', help='Input markup language, as it appears in the input source files')
    parser.add_option('--output-markup', action='store', type='string', dest='markup_output', help='Output markup language, as it will appear in the output source files. If not specified, the input markup will be used.')
    parser.add_option('-l', '--language', action='store', type='string', dest='language', help='Programming language of the source files')
    parser.add_option('-f', '--filter', action='store', type='string', dest='filter', help='Filter to be applied on the input files')
    parser.add_option('-o', '--output', action='store', type='string', dest='path_directory_output', default=path_directory_output_default, help='Output directory, where the output files will be written')
    parser.add_option('-q', '--quiet', action='store_true', dest='quiet', default=False, help='show only critical messages')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='show all messages')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False, help='show ALL messages')


def check_options(options):
    if not os.path.exists(options.path_file_config):
        logger.critical('Configuration file "%s" cannot be found.' % options.path_file_config)
        exit()

# TODO from gage, code for files and directories
def fill_directories(directories, recursive=False):
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
                print ['dir: ' + '|' + directory + '|' + f + '|' + os.path.join(directory, f) for f in os.listdir(directory)]
                inodes_all = [os.path.join(directory, f) for f in os.listdir(directory)]
                directories_all = [d for d in files_sub if os.path.isdir(d)]
                # Add the new directories for the current loop,
                directories.extend(directories_all)
        else:
            logger.error('Error path: the directory "%s" does not exists!' % path_directory)

    print directories_output
    return directories_output


def fill_files(self, directories, extentions):
    files_output = []

    for directory in directories:
        inodes_all = [os.path.join(directory, f) for f in os.listdir(directory)]
        files_all = [f for f in files_sub if os.path.isfile(f) and os.path.splitext(f)[1] in extensions]
        files_output.extend(files_all)

    for file in files_output:
        logger.info('Handling file: "%s"' % file)



if __name__ == '__main__':
    programname = 'doge 0.1'
    optionparser = OptionParser(version=programname)
    set_option_parser(optionparser)
    (options, args) = optionparser.parse_args()

    set_logger(options)
    #check_options(options)

    markup_input = markup.find_markup(options.markup_input, options.language)
    markup_output = markup.find_markup(options.markup_output, options.language)

    if not markup_output:
        markup_output = markup_input

    # TODO pass markup directly instead of assigning to Node
    Node.writer = markup_output.writer
    Node.reader = markup_input.reader
    Node.lang = markup_input.lang

    parser = PythonParser()
    parser.read_file('truc.py')
    parser.print_file()
    parser.build_structure()
    pass
    writer = Writer()
    writer.write(parser.node_file)
    pass
    print ''.join(writer.buffer)
    fill_directories(['/home/ron/code/python/'], recursive=True)
