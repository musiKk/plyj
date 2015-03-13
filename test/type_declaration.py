import unittest
from plyj.model.classes import ClassDeclaration
from plyj.model.file import CompilationUnit
from plyj.model.interface import InterfaceDeclaration
from plyj.model.name import Name
from plyj.model.method import MethodDeclaration
from plyj.model.type import Type
from plyj.parser import Parser


class TypeDeclarationTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_class_inheritance(self):
        m = self.parser.parse_string('''
        class Foo extends Bar implements Baz {
          void foo() {}
        }
        ''')
        cls = self._assert_declaration(m, 'Foo', ClassDeclaration)
        self.assertEquals(cls.extends, Type(Name('Bar')))
        self.assertEquals(cls.implements, [Type(Name('Baz'))])
        self.assertEquals(cls.body, [MethodDeclaration('foo', body=[])])

    def test_class_method(self):
        m = self.parser.parse_string('''
        class Foo {
          void foo() {}
        }
        ''')
        cls = self._assert_declaration(m, 'Foo', ClassDeclaration)
        self.assertEquals(cls.body, [MethodDeclaration('foo', body=[])])

    def test_interface_method(self):
        m = self.parser.parse_string('''
        interface Foo {
          void foo();
        }
        ''')
        cls = self._assert_declaration(m, 'Foo', InterfaceDeclaration)
        self.assertEquals(cls.body.value, [MethodDeclaration('foo', abstract=True)])

    def test_class_abstract_method(self):
        m = self.parser.parse_string('''
        abstract class Foo {
          abstract void foo();
        }
        ''')
        cls = self._assert_declaration(m, 'Foo', ClassDeclaration)
        self.assertEquals(cls.body.value, [
            MethodDeclaration('foo', modifiers=['abstract'], abstract=True)])

    def _assert_declaration(self, compilation_unit, name, declaration_type):
        self.assertIsInstance(compilation_unit, CompilationUnit)
        self.assertTrue(len(compilation_unit.type_declarations) >= 1)

        declaration = compilation_unit.type_declarations[0]
        self.assertIsInstance(declaration, declaration_type)

        self.assertEqual(declaration.name, Name.ensure(name, False))

        return declaration
