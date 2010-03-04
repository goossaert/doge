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
from optparse import OptionParser

import ut
import fs
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
    dir_default_input = './'
    dir_default_output = 'pydoge'
    parser.add_option('-m',
                      '--input-markup',
                      action='store',
                      type='string',
                      dest='markup_input',
                      help='Input markup language, as it appears in the input source files')
    parser.add_option('--output-markup',
                      action='store',
                      type='string',
                      dest='markup_output',
                      help='Output markup language, as it will appear in the output source files. If not specified, the input markup will be used.')
    parser.add_option('-l',
                      '--language',
                      action='store',
                      type='string',
                      dest='language',
                      help='Programming language of the source files')
    parser.add_option('-f',
                      '--filter',
                      action='store',
                      type='string',
                      dest='filter',
                      help='Filter to be applied on the input files')
    parser.add_option('-i',
                      '--input',
                      action='store',
                      type='string',
                      dest='dir_input',
                      default=dir_default_input,
                      help='Input directory, where source files will be read from')
    parser.add_option('-o',
                      '--output',
                      action='store',
                      type='string',
                      dest='dir_output',
                      default=dir_default_output,
                      help='Output directory, where the output files will be written')
    parser.add_option('-r',
                      '--recursive',
                      action='store_true',
                      dest='recursive',
                      default=False,
                      help='Treat the input directory recursively')
    parser.add_option('-q',
                      '--quiet',
                      action='store_true',
                      dest='quiet',
                      default=False,
                      help='show only critical messages')
    parser.add_option('-v',
                      '--verbose',
                      action='store_true',
                      dest='verbose',
                      default=False,
                      help='show all messages')
    parser.add_option('-d',
                      '--debug',
                      action='store_true',
                      dest='debug',
                      default=False,
                      help='show ALL messages')


def check_options(options):
    if not os.path.exists(options.path_file_config):
        logger.critical('Configuration file "%s" cannot be found.' % options.path_file_config)
        exit()


def handle_buffer(buffer):
    markup_input = markup.find_markup('rst', 'python')
    markup_output = markup.find_markup('rst', 'python')

    #print buffer

    if not markup_output:
        markup_output = markup_input

    # TODO pass markup directly instead of assigning to Node
    Node.writer = markup_output.writer
    Node.reader = markup_input.reader
    Node.lang = markup_input.lang

    parser = markup_input.parser
    parser.read_file(buffer)
    parser.print_file()  # what is this for?
    parser.build_structure() # build doc from actual file
    writer = Writer()
    writer.write(parser.node_file)

    return writer.buffer


def handle_standard_io(parser):
    parser.read_file(sys.stdin)
    parser.print_file()  # what is this for?
    parser.build_structure() # build doc from actual file
    writer = Writer()
    writer.write(parser.node_file)
    for line in writer.buffer:
        print line.rstrip()




def handle_files(parser, files, dir_source, dir_dest):
    for filename in files:
        print '--------', filename, '--------'
        file = open(filename, 'r')
        parser.read_file(file)
        file.close()
        parser.print_file()  # what is this for?
        parser.build_structure() # build doc from actual file
        writer = Writer()
        writer.write(parser.node_file)
        filepath = fs.transform_filepath(filename, dir_source, dir_dest)
        print 'path', filename, dir_source, dir_dest, filepath
        file = open(filepath, 'w')
        file.write(''.join(writer.buffer))
        file.close()
        #print ''.join(writer.buffer)




if __name__ == '__main__':
    version = 'doge 0.1'
    optionparser = OptionParser(version=version)
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

    print options.dir_input
    if options.dir_input == '-':
        handle_standard_io(markup_input.parser)
    else:
        directories = fs.get_directories([options.dir_input], options.recursive)
        files = fs.get_files(directories, markup_input.extensions)

        fs.copy_dir_hierarchy(files, options.dir_input, options.dir_output)
        handle_files(markup_input.parser, files, options.dir_input, options.dir_output)
