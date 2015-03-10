import unittest

from plyj.model.expression import *
from plyj.model.statement import *
from plyj.model.type import Type
from plyj.model.variable import Variable, VariableDeclarator
from plyj.parser import Parser


foo = Name('foo')
bar = Name('bar')
i = Name('i')
j = Name('j')
zero = Literal('0')
one = Literal('1')
two = Literal('2')
three = Literal('3')
ten = Literal('10')


class StatementTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_while(self):
        return_block = Block([Return()])
        self.assert_statements({
            'while(foo) return;': While(foo, body=Return()),
            'while(foo) { return; }': While(foo, body=return_block),
            'do return; while(foo);': DoWhile(foo, body=Return()),
            'do { return; } while(foo);': DoWhile(foo, body=return_block)
        })

    def test_for(self):
        initializer = VariableDeclaration('int', [
            VariableDeclarator(Variable('i'), initializer=zero)
        ])
        predicate = BinaryExpression('<', i, ten)
        update = Unary('x++', i)
        initializer2 = [Assignment('=', i, zero), Assignment('=', j, ten)]
        update2 = Unary('x++', j)

        def f(init=None, pred=None, updt=None, body=None):
            return For(init, pred, updt, body)

        self.assert_statements({
            'for(;;);': f(body=Empty()),
            'for(;;) return;': f(body=Return()),
            'for(;;) { return; }': f(body=Block([Return()])),
            'for(int i=0;;) return;': f(init=initializer, body=Return()),
            'for(;i<10;) return;': f(pred=predicate, body=Return()),
            'for(;;i++) return;': f(updt=[update], body=Return()),
            'for(int i=0; i<10; i++) return;': f(initializer, predicate,
                                                 [update], body=Return()),
            'for(i=0, j=10;;) return;': f(init=initializer2, body=Return()),
            'for(;;i++, j++) return;': f(updt=[update, update2],
                                         body=Return()),
            'for(int i : foo) return;':
                ForEach('int', Variable('i'), foo, body=Return())
        })

    def test_assert(self):
        self.assert_statements({
            'assert foo;': Assert(foo),
            'assert foo : "bar";': Assert(foo, message=Literal('"bar"')),
        })

    def test_switch(self):
        default = SwitchCase(['default'], body=[Return()])
        case1 = SwitchCase([one], [Return(one)])
        case12 = SwitchCase([one, two], [Return(three)])

        self.assert_statements({
            'switch(foo) {}': Switch(foo, []),
            'switch(foo) { default: return; }': Switch(foo, [default]),
            'switch(foo) { case 1: return 1; }': Switch(foo, [case1]),
            'switch(foo) { case 1: return 1; default: return; }':
                Switch(foo, [case1, default]),
            'switch(foo) { case 1: case 2: return 3; }': Switch(foo, [case12]),
            'switch(foo) { case 1: case 2: return 3; default: return; }':
                Switch(foo, [case12, default]),
        })

    def test_control_flow(self):
        self.assert_statements({
            'break;': Break(),
            'break label;': Break('label'),

            'continue;': Continue(),
            'continue label;': Continue('label'),

            'return;': Return(),
            'return 1;': Return(one),

            'throw foo;': Throw(foo),
        })

    def test_synchronized(self):
        self.assert_statement('synchronized (foo) { return; }',
                              Synchronized(foo, body=Block([Return()])))

    def test_try(self):
        r1 = Block([Return(one)])
        r2 = Block([Return(two)])
        r3 = Block([Return(three)])
        c1 = Catch(Variable('e'), types=[Type(Name('Exception'))],
                   block=r2)
        c2 = Catch(Variable('e'), types=[Type(Name('Exception1')), Type(
            Name('Exception2'))], block=r3)
        res1 = Resource(Variable('r'),
                        resource_type=Type(Name('Resource')),
                        initializer=Name('foo'))
        res2 = Resource(Variable('r2'),
                        resource_type=Type(Name('Resource2')),
                        initializer=Name('bar'))

        # Try
        t = 'try { return 1; } '
        # Try with resource
        twr = 'try(Resource r = foo) { return 1; } '
        # Try with 2 resources
        tw2r = 'try(Resource r = foo; Resource2 r2 = bar) { return 1; }'
        # Try with 2 resources (B)
        tw2rb = 'try(Resource r = foo; Resource2 r2 = bar;) { return 1; }'
        # Catch
        c = 'catch (Exception e) { return 2; } '
        # Dual Catch
        dc = 'catch (Exception1 | Exception2 e) { return 3; } '
        # Finally
        f = 'finally { return 3; }'

        self.assert_statements({
            t + c:            Try(r1, catches=[c1]),
            t + c + f:        Try(r1, catches=[c1], _finally=r3),
            t + f:            Try(r1, _finally=r3),
            t + dc:           Try(r1, catches=[c2]),
            t + c + dc:       Try(r1, catches=[c1, c2]),
            t + c + dc + f:   Try(r1, catches=[c1, c2], _finally=r3),
            twr:              Try(r1, resources=[res1]),
            tw2r:             Try(r1, resources=[res1, res2]),
            tw2rb:            Try(r1, resources=[res1, res2]),
            twr + c:          Try(r1, resources=[res1], catches=[c1]),
            twr + dc:         Try(r1, resources=[res1], catches=[c2]),
            twr + f:          Try(r1, resources=[res1], _finally=r3),
            twr + c + dc:     Try(r1, resources=[res1], catches=[c1, c2]),

            twr + c + f:      Try(r1, resources=[res1], catches=[c1],
                                  _finally=r3),

            twr + c + dc + f: Try(r1, resources=[res1], catches=[c1, c2],
                                  _finally=r3),
        })

    def test_constructor_invocation(self):
        # Create a helper function to reduce verbosity.
        # t: target, ta: type_arguments, a: arguments
        def ci(name, t=None, ta=None, a=None):
            return ConstructorInvocation(name, t, ta, a)

        foo_type = Type(Name('Foo'))
        bar_type = Type(Name('Bar'))
        bar_lit = Literal('"bar"')

        for c in ['super', 'this']:
            c_call = c + "();"
            self.assert_statements({
                c + '();':               ci(c),
                c + '(1);':              ci(c, a=[one]),
                c + '(1, foo, "bar");':  ci(c, a=[one, foo, bar_lit]),
                '<Foo>' + c_call:        ci(c, ta=[foo_type]),
                'Foo.' + c_call:         ci(c, t=Name('Foo')),
                'Foo.<Bar>' + c_call:    ci(c, ta=[bar_type], t=Name('Foo'))
            })

    def test_if(self):
        r1 = Return(one)
        r2 = Return(two)

        self.assert_statements({
            'if(foo) return;': IfThenElse(foo, if_true=Return()),
            'if(foo) { return; }': IfThenElse(foo, if_true=Block([Return()])),

            'if(foo) return 1; else return 2;':
                IfThenElse(foo, if_true=r1, if_false=r2),
            'if(foo) {return 1;} else return 2;':
                IfThenElse(foo, if_true=Block([r1]), if_false=r2),
            'if(foo) return 1; else {return 2;}':
                IfThenElse(foo, if_true=r1, if_false=Block([r2])),
            'if(foo) {return 1;} else {return 2;}':
                IfThenElse(foo, if_true=Block([r1]), if_false=Block([r2])),

            # test proper nesting, every parser writer's favorite
            'if(foo) if(bar) return 1;':
                IfThenElse(foo, if_true=IfThenElse(bar, if_true=r1)),
            'if(foo) if(bar) return 1; else return 2;':
                IfThenElse(foo, if_true=IfThenElse(bar,
                                                   if_true=r1,
                                                   if_false=r2)),
            'if(foo) return 1; else if(bar) return 2;':
                IfThenElse(foo, if_true=r1, if_false=IfThenElse(bar,
                                                                if_true=r2)),
        })

    def test_variable_declaration(self):
        var_i = Variable('i')
        var_i_declarator = VariableDeclarator(var_i)
        var_j = Variable('j')
        var_j_declarator = VariableDeclarator(var_j)

        # i declarator array
        ida = [var_i_declarator]
        # i, j declarator array
        ijda = [var_i_declarator, var_j_declarator]

        self.assert_statement('int i;', VariableDeclaration('int', ida))
        self.assert_statement('int i, j;', VariableDeclaration('int', ijda))

        var_i_declarator.initializer = one
        self.assert_statement('int i = 1;', VariableDeclaration('int', ida))
        self.assert_statement('int i = 1, j;',
                              VariableDeclaration('int', ijda))

        var_j_declarator.initializer = i
        self.assert_statement('int i = 1, j = i;',
                              VariableDeclaration('int', ijda))

        int_ar = Type('int', dimensions=1)
        var_i_declarator.initializer = None
        self.assert_statement('int[] i;', VariableDeclaration(int_ar, ida))

    def test_array(self):
        var_i = Variable('i')
        var_i_declarator = VariableDeclarator(var_i)

        int_ar = Type('int', dimensions=1)

        arr_init = ArrayInitializer([one, three])
        var_i_declarator.initializer = arr_init
        self.assert_statement('int[] i = {1, 3};',
                              VariableDeclaration(int_ar, [var_i_declarator]))

        arr_creation = ArrayCreation('int', dimensions=[None],
                                     initializer=arr_init)
        var_i_declarator.initializer = arr_creation
        self.assert_statement('int[] i = new int[] {1, 3};',
                              VariableDeclaration(int_ar, [var_i_declarator]))

        arr_creation.dimensions = [two]
        self.assert_statement('int[] i = new int[2] {1, 3};',
                              VariableDeclaration(int_ar, [var_i_declarator]))

    def test_empty(self):
        self.assert_statement(';', Empty())

    def assert_statements(self, statements):
        for test, expected in statements.iteritems():
            self.assert_statement(test, expected)

    def assert_statement(self, stmt, result):
        s = self.parser.parse_statement(stmt)
        message = 'for {} got {}, expected {}'.format(stmt, s, result)
        self.assertEqual(s, result, message)
