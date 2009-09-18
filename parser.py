import io
import re

class Parser:
    def __init__(self):
        self.module = None

    def read_file(self, name_file):
        file = open(name_file, 'r')

        pattern_class = re.compile(
            r"""
            (?P<indent>[\s]*?)
            class.*?
            """, re.VERBOSE | re.DOTALL)

        pattern_function = re.compile(
            r"""
            (?P<indent>[\s]*?)
            def.*?
            """, re.VERBOSE | re.DOTALL)

        in_class = []
        in_function = []
        for line in file:
            if pattern_class.match(line) 
            pass   
