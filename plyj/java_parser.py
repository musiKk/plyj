#!/usr/bin/env python2
from plyj.java_lexer import JavaLexer

from plyj.parsers.class_parser import ClassParser
from plyj.parsers.compilation_unit_parser import CompilationUnitParser
from plyj.parsers.expression_parser import ExpressionParser
from plyj.parsers.literal_parser import LiteralParser
from plyj.parsers.name_parser import NameParser
from plyj.parsers.statement_parser import StatementParser
from plyj.parsers.type_parser import TypeParser


class JavaParser(ExpressionParser, NameParser, LiteralParser, TypeParser,
                 ClassParser, StatementParser, CompilationUnitParser):
    """
    There should be no reason to use this class directly. Please use Parser in
    parser.py

    This class implements the Java parser for YACC.
    """
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