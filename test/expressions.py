import unittest

import plyj.parser as plyj
import plyj.model as model

def b(operator, operand1, operand2):
    return model.BinaryExpression(operator, operand1, operand2)

def u(operator, operand):
    return model.Unary(operator, operand)

expression_tests = [
    # simple test for each operator
    ('1+2', b('+', '1', '2')),
    (' 1 + 2 ', b('+', '1', '2')),
    ('1-2', b('-', '1', '2')),
    ('1*2', b('*', '1', '2')),
    ('1/2', b('/', '1', '2')),
    ('1%2', b('%', '1', '2')),
    ('1^2', b('^', '1', '2')),
    ('1&2', b('&', '1', '2')),
    ('1&&2', b('&&', '1', '2')),
    ('1|2', b('|', '1', '2')),
    ('1||2', b('||', '1', '2')),
    ('1==2', b('==', '1', '2')),
    ('1!=2', b('!=', '1', '2')),
    ('1<2', b('<', '1', '2')),
    ('1<=2', b('<=', '1', '2')),
    ('1>2', b('>', '1', '2')),
    ('1>=2', b('>=', '1', '2')),
    ('1<<2', b('<<', '1', '2')),
    ('1>>2', b('>>', '1', '2')),
    ('1>>>2', b('>>>', '1', '2')),
    # left associativity
    ('1+2+3', b('+', b('+', '1', '2'), '3')),
    # precedence
    ('1+2*3', b('+', '1', b('*', '2', '3'))),
    # parenthesized expressions
    ('(1+2)*3', b('*', b('+', '1', '2'), '3')),
    # conditionals
    ('a ? b : c', model.Conditional('a', 'b', 'c')),
    ('a ? b ? c : d : e', model.Conditional('a', model.Conditional('b', 'c', 'd'), 'e')),
    ('a ? b : c ? d : e', model.Conditional('a', 'b', model.Conditional('c', 'd', 'e'))),
    # unary expressions
    ('+a', u('+', 'a')),
    ('-a', u('-', 'a')),
    ('!a', u('!', 'a')),
    ('!!a', u('!', u('!', 'a'))),
    ('~a', u('~', 'a')),
    ('++a', u('++x', 'a')),
    ('--a', u('--x', 'a')),
    ('a++', u('x++', 'a')),
    ('a--', u('x--', 'a')),
    # assignment expressions
    ('a = 1', model.Assignment('=', 'a', '1')),
    ('a += 1', model.Assignment('+=', 'a', '1')),
    ('a -= 1', model.Assignment('-=', 'a', '1')),
    ('a *= 1', model.Assignment('*=', 'a', '1')),
    ('a /= 1', model.Assignment('/=', 'a', '1')),
    ('a %= 1', model.Assignment('%=', 'a', '1')),
    ('a ^= 1', model.Assignment('^=', 'a', '1')),
    ('a &= 1', model.Assignment('&=', 'a', '1')),
    ('a |= 1', model.Assignment('|=', 'a', '1')),
    ('a <<= 1', model.Assignment('<<=', 'a', '1')),
    ('a >>= 1', model.Assignment('>>=', 'a', '1')),
    ('a >>>= 1', model.Assignment('>>>=', 'a', '1')),
]

class ExpressionTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

    def test_expressions(self):
        for expr, result in expression_tests:
            t = self.parser.parse_expression(expr)
            self.assertEquals(t, result, 'for {} got: {}, expected: {}'.format(expr, t, result))

if __name__ == '__main__':
    unittest.main()
