#!/usr/bin/env python2


class JavaLexer(object):
    """
    There should be no reason to use this class directly. Please use Parser in
    parser.py

    This class implements the Java lexer for Lex.
    """

    keywords = ('this', 'class', 'void', 'super', 'extends', 'implements',
                'enum', 'interface', 'byte', 'short', 'int', 'long', 'char',
                'float', 'double', 'boolean', 'null', 'true', 'false', 'final',
                'public', 'protected', 'private', 'abstract', 'static',
                'strictfp', 'transient', 'volatile', 'synchronized', 'native',
                'throws', 'default', 'instanceof', 'if', 'else', 'while',
                'for', 'switch', 'case', 'assert', 'do', 'break', 'continue',
                'return', 'throw', 'try', 'catch', 'finally', 'new', 'package',
                'import')

    tokens = ['NAME', 'NUM',

              'CHAR_LITERAL', 'STRING_LITERAL',

              'LINE_COMMENT', 'BLOCK_COMMENT',

              'OR', 'AND',
              'EQ', 'NEQ', 'GTEQ', 'LTEQ',
              'LSHIFT', 'RSHIFT', 'RRSHIFT',

              'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'REMAINDER_ASSIGN',
              'PLUS_ASSIGN', 'MINUS_ASSIGN', 'LSHIFT_ASSIGN', 'RSHIFT_ASSIGN',
              'RRSHIFT_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN',

              'PLUSPLUS', 'MINUSMINUS',

              'ELLIPSIS'] + [k.upper() for k in keywords]

    literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

    t_NUM = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
    t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
    t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

    t_ignore_LINE_COMMENT = '//.*'

    @staticmethod
    def t_BLOCK_COMMENT(t):
        r"""/\*(.|\n)*?\*/"""
        t.lexer.lineno += t.value.count('\n')

    t = 0

    t_OR = r'\|\|'
    t_AND = '&&'

    t_EQ = '=='
    t_NEQ = '!='
    t_GTEQ = '>='
    t_LTEQ = '<='

    t_LSHIFT = '<<'
    t_RSHIFT = '>>'
    t_RRSHIFT = '>>>'

    t_TIMES_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = '/='
    t_REMAINDER_ASSIGN = '%='
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = '-='
    t_LSHIFT_ASSIGN = '<<='
    t_RSHIFT_ASSIGN = '>>='
    t_RRSHIFT_ASSIGN = '>>>='
    t_AND_ASSIGN = '&='
    t_OR_ASSIGN = r'\|='
    t_XOR_ASSIGN = '\^='

    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'\-\-'

    t_ELLIPSIS = r'\.\.\.'

    t_ignore = ' \t\f'

    @staticmethod
    def t_NAME(t):
        """[A-Za-z_$][A-Za-z0-9_$]*"""
        if t.value in JavaLexer.keywords:
            t.type = t.value.upper()
        return t

    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    @staticmethod
    def t_newline_win(t):
        r"""(\r\n)+"""
        t.lexer.lineno += len(t.value) / 2

    @staticmethod
    def t_error(t):
        print("Illegal character '{}' ({}) in line {}"
              .format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        t.lexer.skip(1)