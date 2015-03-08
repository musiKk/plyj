#!/usr/bin/env python2
from plyj.model import Name


class NameParser(object):
    @staticmethod
    def p_name(p):
        """name : simple_name
                | qualified_name"""
        p[0] = p[1]

    @staticmethod
    def p_simple_name(p):
        """simple_name : NAME"""
        p[0] = Name(p[1])

    @staticmethod
    def p_qualified_name(p):
        """qualified_name : name '.' simple_name"""
        p[1].append_name(p[3])
        p[0] = p[1]