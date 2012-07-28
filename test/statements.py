import unittest

import plyj.parser as plyj
import plyj.model as model

class StatementTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

    def test_while(self):
        self.assert_stmt('while(foo) return;', model.While('foo', body=model.Return()))
        self.assert_stmt('while(foo) { return; }', model.While('foo', body=[model.Return()]))

        self.assert_stmt('do return; while(foo);', model.DoWhile('foo', body=model.Return()))
        self.assert_stmt('do { return; } while(foo);', model.DoWhile('foo', body=[model.Return()]))

    def test_for(self):
        initializer = model.VariableDeclaration('int', [model.VariableDeclarator(model.Variable('i'), initializer='0')])
        predicate = model.BinaryExpression('<', 'i', '10')
        update = model.Unary('x++', 'i')

        self.assert_stmt('for(;;) return;', model.For(None, None, None, body=model.Return()))
        self.assert_stmt('for(;;) { return; }', model.For(None, None, None, body=[model.Return()]))
        self.assert_stmt('for(int i=0;;) return;', model.For(initializer, None, None, body=model.Return()))
        self.assert_stmt('for(;i<10;) return;', model.For(None, predicate, None, body=model.Return()))
        self.assert_stmt('for(;;i++) return;', model.For(None, None, [update], body=model.Return()))
        self.assert_stmt('for(int i=0; i<10; i++) return;', model.For(initializer, predicate, [update], body=model.Return()))

        initializer2 = [model.Assignment('=', 'i', '0'), model.Assignment('=', 'j', '2')]
        self.assert_stmt('for(i=0, j=2;;) return;', model.For(initializer2, None, None, body=model.Return()))

        update2 = model.Unary('x++', 'j')
        self.assert_stmt('for(;;i++, j++) return;', model.For(None, None, [update, update2], body=model.Return()))

    def test_if(self):
        self.assert_stmt('if(foo) return;', model.IfThenElse('foo', if_true=model.Return()))
        self.assert_stmt('if(foo) { return; }', model.IfThenElse('foo', if_true=[model.Return()]))

        r1 = model.Return(result='1')
        r2 = model.Return(result='2')
        self.assert_stmt('if(foo) return 1; else return 2;', model.IfThenElse('foo', if_true=r1, if_false=r2))
        self.assert_stmt('if(foo) {return 1;} else return 2;', model.IfThenElse('foo', if_true=[r1], if_false=r2))
        self.assert_stmt('if(foo) return 1; else {return 2;}', model.IfThenElse('foo', if_true=r1, if_false=[r2]))
        self.assert_stmt('if(foo) {return 1;} else {return 2;}', model.IfThenElse('foo', if_true=[r1], if_false=[r2]))

        # test proper nesting, every parser writer's favorite
        self.assert_stmt('if(foo) if(bar) return 1;', model.IfThenElse('foo', if_true=model.IfThenElse('bar', if_true=r1)))
        self.assert_stmt('if(foo) if(bar) return 1; else return 2;',
                         model.IfThenElse('foo', if_true=model.IfThenElse('bar', if_true=r1, if_false=r2)))
        self.assert_stmt('if(foo) return 1; else if(bar) return 2;',
                         model.IfThenElse('foo', if_true=r1, if_false=model.IfThenElse('bar', if_true=r2)))

    def test_variable_declaration(self):
        var_i = model.Variable('i')
        var_i_decltor = model.VariableDeclarator(var_i)
        var_j = model.Variable('j')
        var_j_decltor = model.VariableDeclarator(var_j)

        self.assert_stmt('int i;', model.VariableDeclaration('int', [var_i_decltor]))
        self.assert_stmt('int i, j;', model.VariableDeclaration('int', [var_i_decltor, var_j_decltor]))

        var_i_decltor.initializer = '1'
        self.assert_stmt('int i = 1;', model.VariableDeclaration('int', [var_i_decltor]))
        self.assert_stmt('int i = 1, j;', model.VariableDeclaration('int', [var_i_decltor, var_j_decltor]))

        var_j_decltor.initializer = 'i'
        self.assert_stmt('int i = 1, j = i;', model.VariableDeclaration('int', [var_i_decltor, var_j_decltor]))

        int_ar = model.Type('int', dimensions=1)
        var_i_decltor.initializer = None
        self.assert_stmt('int[] i;', model.VariableDeclaration(int_ar, [var_i_decltor]))

    def test_array(self):
        var_i = model.Variable('i')
        var_i_decltor = model.VariableDeclarator(var_i)
        var_j = model.Variable('j')
        var_j_decltor = model.VariableDeclarator(var_j)

        int_ar = model.Type('int', dimensions=1)

        arr_init = model.ArrayInitializer(['1', '3'])
        var_i_decltor.initializer = arr_init
        self.assert_stmt('int[] i = {1, 3};', model.VariableDeclaration(int_ar, [var_i_decltor]))

        arr_creation = model.ArrayCreation('int', dimensions=[None], initializer=arr_init)
        var_i_decltor.initializer = arr_creation
        self.assert_stmt('int[] i = new int[] {1, 3};', model.VariableDeclaration(int_ar, [var_i_decltor]))

        arr_creation.dimensions = ['2']
        self.assert_stmt('int[] i = new int[2] {1, 3};', model.VariableDeclaration(int_ar, [var_i_decltor]))

    def assert_stmt(self, stmt, result):
        s = self.parser.parse_statement(stmt)
        self.assertEqual(s, result, 'for {} got {}, expected {}'.format(stmt, s, result))
