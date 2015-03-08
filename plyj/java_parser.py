#!/usr/bin/env python2
from java_lexer import JavaLexer

from parsers.class_parser import ClassParser
from parsers.compilation_unit_parser import CompilationUnitParser
from parsers.expression_parser import ExpressionParser
from parsers.literal_parser import LiteralParser
from parsers.name_parser import NameParser
from parsers.statement_parser import StatementParser
from parsers.type_parser import TypeParser


class JavaParser(ExpressionParser, NameParser, LiteralParser, TypeParser,
                 ClassParser, StatementParser, CompilationUnitParser):
    tokens = JavaLexer.tokens

    @staticmethod
    def p_goal_compilation_unit(p):
        """goal : PLUSPLUS compilation_unit"""
        p[0] = p[2]

    @staticmethod
    def p_goal_expression(p):
        """goal : MINUSMINUS expression"""
        p[0] = p[2]

    @staticmethod
    def p_goal_statement(p):
        """goal : '*' block_statement"""
        p[0] = p[2]

    @staticmethod
    def p_error(p):
        print('error: {}'.format(p))

    @staticmethod
    def p_empty(p):
        """empty :"""