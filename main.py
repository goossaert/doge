from parser import Parser 

if __name__ == '__main__':
    parser = Parser()
    parser.read_file('parser.py')
    parser.print_file()
