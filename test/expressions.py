import unittest

import plyj.parser as plyj
import plyj.model as model

one = model.Literal('1')
two = model.Literal('2')
three = model.Literal('3')
a = model.Name('a')
b = model.Name('b')
c = model.Name('c')
d = model.Name('d')
e = model.Name('e')

def bin(operator, operand1, operand2):
    return model.BinaryExpression(operator, operand1, operand2)

def u(operator, operand):
    return model.Unary(operator, operand)

expression_tests = [
    # simple test for each operator
    ('1+2', bin('+', one, two)),
    (' 1 + 2 ', bin('+', one, two)),
    ('1-2', bin('-', one, two)),
    ('1*2', bin('*', one, two)),
    ('1/2', bin('/', one, two)),
    ('1%2', bin('%', one, two)),
    ('1^2', bin('^', one, two)),
    ('1&2', bin('&', one, two)),
    ('1&&2', bin('&&', one, two)),
    ('1|2', bin('|', one, two)),
    ('1||2', bin('||', one, two)),
    ('1==2', bin('==', one, two)),
    ('1!=2', bin('!=', one, two)),
    ('1<2', bin('<', one, two)),
    ('1<=2', bin('<=', one, two)),
    ('1>2', bin('>', one, two)),
    ('1>=2', bin('>=', one, two)),
    ('1<<2', bin('<<', one, two)),
    ('1>>2', bin('>>', one, two)),
    ('1>>>2', bin('>>>', one, two)),
    # left associativity
    ('1+2+3', bin('+', bin('+', one, two), three)),
    # precedence
    ('1+2*3', bin('+', one, bin('*', two, three))),
    # parenthesized expressions
    ('(1+2)*3', bin('*', bin('+', one, two), three)),
    # conditionals
    ('a ? b : c', model.Conditional(a, b, c)),
    ('a ? b ? c : d : e', model.Conditional(a, model.Conditional(b, c, d), e)),
    ('a ? b : c ? d : e', model.Conditional(a, b, model.Conditional(c, d, e))),
    # unary expressions
    ('+a', u('+', a)),
    ('-a', u('-', a)),
    ('!a', u('!', a)),
    ('!!a', u('!', u('!', a))),
    ('~a', u('~', a)),
    ('++a', u('++x', a)),
    ('--a', u('--x', a)),
    ('a++', u('x++', a)),
    ('a--', u('x--', a)),
    # assignment expressions
    ('a = 1', model.Assignment('=', a, one)),
    ('a += 1', model.Assignment('+=', a, one)),
    ('a -= 1', model.Assignment('-=', a, one)),
    ('a *= 1', model.Assignment('*=', a, one)),
    ('a /= 1', model.Assignment('/=', a, one)),
    ('a %= 1', model.Assignment('%=', a, one)),
    ('a ^= 1', model.Assignment('^=', a, one)),
    ('a &= 1', model.Assignment('&=', a, one)),
    ('a |= 1', model.Assignment('|=', a, one)),
    ('a <<= 1', model.Assignment('<<=', a, one)),
    ('a >>= 1', model.Assignment('>>=', a, one)),
    ('a >>>= 1', model.Assignment('>>>=', a, one)),
]

class ExpressionTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

    def test_expressions(self):
        for expr, result in expression_tests:
            t = self.parser.parse_expression(expr)
            self.assertEqual(t, result, 'for {} got: {}, expected: {}'.format(expr, t, result))

if __name__ == '__main__':
    unittest.main()
