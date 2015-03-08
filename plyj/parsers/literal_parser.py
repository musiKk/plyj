#!/usr/bin/env python2
from plyj.model import Literal


class LiteralParser(object):
    @staticmethod
    def p_literal(p):
        """literal : NUM
                   | CHAR_LITERAL
                   | STRING_LITERAL
                   | TRUE
                   | FALSE
                   | NULL"""
        p[0] = Literal(p[1])