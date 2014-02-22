import unittest

import plyj.parser as plyj
import plyj.model as model
from plyj.model import *

class TypeDeclarationTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

    def test_class_method(self):
        m = self.parser.parse_string('''
        class Foo {
          void foo() {}
        }
        ''')
        cls = self._assert_declaration(m, 'Foo')
        self.assertEquals(cls.body, [MethodDeclaration('foo', body=[])])

    def test_interface_method(self):
        m = self.parser.parse_string('''
        interface Foo {
          void foo();
        }
        ''')
        cls = self._assert_declaration(m, 'Foo', type=model.InterfaceDeclaration)
        self.assertEquals(cls.body, [MethodDeclaration('foo', abstract=True)])

    def test_class_abstract_method(self):
        m = self.parser.parse_string('''
        abstract class Foo {
          abstract void foo();
        }
        ''')
        cls = self._assert_declaration(m, 'Foo')
        self.assertEquals(cls.body, [MethodDeclaration('foo', modifiers=['abstract'], abstract=True)])

    def _assert_declaration(self, compilation_unit, name, index=0, type=model.ClassDeclaration):
        self.assertIsInstance(compilation_unit, model.CompilationUnit)
        self.assertTrue(len(compilation_unit.type_declarations) >= index + 1)

        decl = compilation_unit.type_declarations[index]
        self.assertIsInstance(decl, type)

        self.assertEqual(decl.name, name)

        return decl
