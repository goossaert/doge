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
    path_file_config_default = 'rules.cfg'
    parser.add_option('-c', '--config', action='store', type='string', dest='path_file_config', default=path_file_config_default, help='Configuration file, where the rules will be read')
    path_directory_output_default = 'gateway'
    parser.add_option('-o', '--output', action='store', type='string', dest='path_directory_output', default=path_directory_output_default, help='Output directory, where the output files will be written')
    parser.add_option('-q', '--quiet', action='store_true', dest='quiet', default=False, help='show only critical messages')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='show all messages')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False, help='show ALL messages')


def check_options(options):
    if not os.path.exists(options.path_file_config):
        logger.critical('Configuration file "%s" cannot be found.' % options.path_file_config)
        exit()

    # TODO from gage, code for files and directories
    def fill_directories(self, name_directory_base):
        #self.path_directory_output = None
        paths_directory_input = []
        for rule_directory in self.rule_set.get_rules_by_type('RuleDirectoryPermission'):
            if rule_directory.action == 'input':
                paths_directory_input.append(os.path.join(name_directory_base, rule_directory.name_directory))
            #elif not self.path_directory_output: # action == 'output'
            #    pass

        paths_directory_input_loop = paths_directory_input if paths_directory_input else ['./']

        #if not self.path_directory_output:
        #    self.path_directory_output = self.path_directory_output_default
        #    logger.warning('No output directory given, using default: "%s"' % self.path_directory_output)

        while paths_directory_input_loop:
            path_directory = paths_directory_input_loop.pop()
            if os.path.exists(path_directory):
                paths_directory_sub = [os.path.join(path_directory, f) for f in os.listdir(path_directory) if os.path.isdir(os.path.join(path_directory, f))]
                # Add the new directories for the current loop,
                paths_directory_input_loop.extend(paths_directory_sub)
                # Save the popped directory
                self.paths_directory_input.append(path_directory)
                logger.info('Handling directory: "%s"' % path_directory)
                #self.paths_directory_input.extend(paths_directory_sub)
            else:
                logger.error('Error path: the directory "%s" does not exists!' % path_directory)


    def fill_files(self):
        for path_directory in self.paths_directory_input:
            paths_files = [f for f in os.listdir(path_directory) if os.path.isfile(os.path.join(path_directory, f))]
            paths_files_valid = [os.path.join(path_directory, f) for f in paths_files if self.rule_set.check_permission('RuleFilePermission', {'name_file': f})]
            self.paths_file_input.extend(paths_files_valid)

        # Logs
        for path in self.paths_file_input:
            logger.info('Handling file: "%s"' % path)




if __name__ == '__main__':
    optionparser = OptionParser(version="doge 0.1")
    set_option_parser(optionparser)
    (options, args) = optionparser.parse_args()

    set_logger(options)
    #check_options(options)

    Node.writer = RestructuredTextWriter()
    Node.reader = RestructuredTextReader()
    Node.lang = PythonLang()

    parser = PythonParser()
    parser.read_file('truc.py')
    parser.print_file()
    parser.build_structure()
    pass
    writer = Writer()
    writer.write(parser.node_file)
    pass
    print ''.join(writer.buffer)
