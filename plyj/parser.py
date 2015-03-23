#!/usr/bin/env python2
from ply import lex as lex, yacc
import sys
from plyj.java_lexer import JavaLexer
from plyj.java_parser import JavaParser


class Parser(object):
    def __init__(self):
        self.lexer = lex.lex(module=JavaLexer(), optimize=1)
        self.parser = yacc.yacc(module=JavaParser(), start='goal', optimize=1)

    def tokenize_string(self, code):
        self.lexer.input(code)
        for token in self.lexer:
            print(token)

    def tokenize_file(self, _file):
        if type(_file) == str:
            _file = open(_file)
        content = ''
        for line in _file:
            content += line
        return self.tokenize_string(content)

    def parse_expression(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='--')

    def parse_statement(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='* ')

    def parse_string(self, code, debug=0, lineno=1, prefix='++'):
        self.lexer.lineno = lineno
        return self.parser.parse(prefix + code, lexer=self.lexer, debug=debug)

    def parse_file(self, file_, debug=0):
        if isinstance(file_, str):
            if sys.version_info[0] == 2:
                # Python 2: Read as raw bytes. There are things like
                # "isinstance(x, str)" in the code which fail if we read it as
                # unicode. I'd fix that instead of this, but Java doesn't
                # make use of unicode as part of its syntax.
                with open(file_) as file_obj_:
                    content = file_obj_.read()
            else:
                # Python 3: Read as unicode.
                with open(file_, "rb") as file_obj_:
                    content = file_obj_.read().decode('utf8', 'ignore')
        else:
            content = file_.read()
        return self.parse_string(content, debug=debug)