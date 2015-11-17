import unittest

import plyj.parser as plyj
import plyj.model as model


class VisitorTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

    def test_visit_expressions_in_try_catch(self):
        statement = '''
        try {
            b = c;
        } catch(Exception e) {
            method(1, 2);
        }
        '''
        s = self.parser.parse_statement(statement)

        class TestVisitor(model.Visitor):
            def __init__(self):
                super(TestVisitor, self).__init__()
                self._count = 0

            def visit_ExpressionStatement(self, expression_statement):
                self._count += 1
                return True

        visitor = TestVisitor()
        s.accept(visitor)
        self.assertEqual(visitor._count, 2,
                         'for {} \nNumber of Expressions got: {}, expected: {}'.format(statement, visitor._count, 2))
