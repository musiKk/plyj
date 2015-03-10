#!/usr/bin/env python2
from plyj.model.literal import Literal
from plyj.model.source_element import collect_tokens


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
        collect_tokens(p)