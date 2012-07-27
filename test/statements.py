import unittest

import plyj.parser as plyj
import plyj.model as model

class StatementTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

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

    def test_assignment(self):
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
