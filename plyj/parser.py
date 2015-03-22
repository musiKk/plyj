#!/usr/bin/env python2
from ply import lex as lex, yacc
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
            with open(file_) as file_obj_:
                content = file_obj_.read()
        else:
            content = file_.read()
        return self.parse_string(content, debug=debug)