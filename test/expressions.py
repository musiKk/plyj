import unittest
from plyj.model.expression import *
from plyj.model.literal import Literal, ClassLiteral
from plyj.model.name import Name
from plyj.model.type import Type
from plyj.parser import Parser

one = Literal('1')
two = Literal('2')
three = Literal('3')
a = Name('a')
b = Name('b')
c = Name('c')
d = Name('d')
e = Name('e')
Foo = Name('Foo')
foo = Name('foo')
T = Name('T')
bar = Name('Bar')

def u(operator, operand):
    return Unary(operator, operand)

expression_tests = [
    # simple test for each operator
    ('1+2', Additive('+', one, two)),
    (' 1 + 2 ', Additive('+', one, two)),
    ('1-2', Additive('-', one, two)),
    ('1*2', Multiplicative('*', one, two)),
    ('1/2', Multiplicative('/', one, two)),
    ('1%2', Multiplicative('%', one, two)),
    ('1^2', Xor('^', one, two)),
    ('1&2', And('&', one, two)),
    ('1&&2', ConditionalAnd('&&', one, two)),
    ('1|2', Or('|', one, two)),
    ('1||2', ConditionalOr('||', one, two)),
    ('1==2', Equality('==', one, two)),
    ('1!=2', Equality('!=', one, two)),
    ('1<2', Relational('<', one, two)),
    ('1<=2', Relational('<=', one, two)),
    ('1>2', Relational('>', one, two)),
    ('1>=2', Relational('>=', one, two)),
    ('1<<2', Shift('<<', one, two)),
    ('1>>2', Shift('>>', one, two)),
    ('1>>>2', Shift('>>>', one, two)),

    # left associativity
    ('1+2+3', Additive('+', Additive('+', one, two), three)),

    # precedence
    ('1+2*3', Additive('+', one, Multiplicative('*', two, three))),

    # parenthesized expressions
    ('(1+2)*3', Multiplicative('*',
                               BracketedExpression(Additive('+', one, two)),
                               three)),

    # conditionals
    ('a ? b : c', Conditional(a, b, c)),
    ('a ? b ? c : d : e', Conditional(a, Conditional(b, c, d), e)),
    ('a ? b : c ? d : e', Conditional(a, b, Conditional(c, d, e))),

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
    ('a = 1', Assignment('=', a, one)),
    ('a += 1', Assignment('+=', a, one)),
    ('a -= 1', Assignment('-=', a, one)),
    ('a *= 1', Assignment('*=', a, one)),
    ('a /= 1', Assignment('/=', a, one)),
    ('a %= 1', Assignment('%=', a, one)),
    ('a ^= 1', Assignment('^=', a, one)),
    ('a &= 1', Assignment('&=', a, one)),
    ('a |= 1', Assignment('|=', a, one)),
    ('a <<= 1', Assignment('<<=', a, one)),
    ('a >>= 1', Assignment('>>=', a, one)),
    ('a >>>= 1', Assignment('>>>=', a, one)),

    # casts
    ('(Foo) a', Cast(Type(Foo), a)),
    ('(int[]) a', Cast(Type('int', dimensions=1), a)),
    ('(Foo[]) a', Cast(Type(Foo, dimensions=1), a)),
    ('(Foo<T>) a', Cast(Type(Foo, type_arguments=[Type(T)]), a)),
    ('(Foo<T>.Bar) a',
        Cast(Type(bar, enclosed_in=Type(Foo, type_arguments=[Type(T)])), a)),

    # method invocation
    ('foo.bar()', MethodInvocation(name='bar', target=foo)),
    ('foo.class.getName()', MethodInvocation(target=ClassLiteral(Type(foo)),
                                             name='getName')),
    ('foo.Class[].class', ClassLiteral(Type(Name('foo.Class'), dimensions=1)))
]


class ExpressionTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_expressions(self):
        for expr, result in expression_tests:
            t = self.parser.parse_expression(expr)
            message = 'for {} got: {}, expected: {}'.format(expr, t, result)
            self.assertEqual(t, result, message)

if __name__ == '__main__':
    unittest.main()
