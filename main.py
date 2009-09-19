from file_parser import Parser
from writer import Writer

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

