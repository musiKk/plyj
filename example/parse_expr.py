#!/usr/bin/env python2

import sys
from plyj.parser import Parser

if len(sys.argv) == 1:
    print('''usage: parse_expr.py <expression> ...
   Example: parse_expr.py '1+2' '3' 'j = (int) i + 3' ''')
    sys.exit(1)

parser = Parser()
for expr in sys.argv[1:]:
    print(parser.parse_expression(expr))

