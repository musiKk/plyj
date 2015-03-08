import unittest
from plyj.model.annotation import Annotation, AnnotationMember
from plyj.model.classes import ClassDeclaration
from plyj.model.file import CompilationUnit, ImportDeclaration, PackageDeclaration
from plyj.model.literal import Literal, Name
from plyj.parser import Parser
from plyj.visitor import Visitor


class CompilationUnitTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_class(self):
        m = self.parser.parse_string('''
        class Foo {}
        ''')
        cls = self._assert_declaration(m, 'Foo')
        self.assertEqual(len(cls.modifiers), 0)

    def test_class_modifiers(self):
        m = self.parser.parse_string('''
        public static final class Foo {}
        ''')
        cls = self._assert_declaration(m, 'Foo')
        self.assertEqual(cls.modifiers, ['public', 'static', 'final'])

    def test_default_package(self):
        m = self.parser.parse_string('''
        class Foo {}
        ''')
        self.assertIsNone(m.package_declaration)

    def test_package(self):
        m = self.parser.parse_string('''
        package foo.bar;
        ''')
        self.assertEqual(m.package_declaration, PackageDeclaration(
            Name('foo.bar')))

    def test_package_annotation(self):
        m = self.parser.parse_string('''
        @Annot
        package foo;
        ''')
        self.assertEqual(m.package_declaration,
                         PackageDeclaration(Name('foo'),
                                            modifiers=[Annotation(
                                                Name('Annot'))]))

    def test_import(self):
        m = self.parser.parse_string('''
        import foo;
        import foo.bar;
        ''')
        self.assertEqual(m.import_declarations,
                         [ImportDeclaration(Name('foo')),
                          ImportDeclaration(Name('foo.bar'))])

    def test_static_import(self):
        m = self.parser.parse_string('''
        import static foo.bar;
        ''')
        self.assertEqual(m.import_declarations,
                         [ImportDeclaration(Name('foo.bar'), static=True)])

    def test_wildcard_import(self):
        m = self.parser.parse_string('''
        import foo.bar.*;
        ''')
        self.assertEqual(m.import_declarations,
                         [ImportDeclaration(Name('foo.bar'), on_demand=True)])

    def test_static_wildcard_import(self):
        m = self.parser.parse_string('''
        import static foo.bar.*;
        ''')
        self.assertEqual(m.import_declarations,
                         [
                             ImportDeclaration(Name('foo.bar'), static=True,
                                               on_demand=True)])

    def test_annotations(self):
        # bug #13
        m = self.parser.parse_string('''
        @Annot(key = 1)
        class Foo {}
        ''')
        t = self._assert_declaration(m, 'Foo')

        self.assertEqual(t.modifiers, [Annotation(
            name=Name('Annot'),
            members=[AnnotationMember(name=Name('key'),
                                      value=Literal('1'))])])

    def test_line_comment(self):
        m = self.parser.parse_string(r'''
        class Foo {}
        //
        //\
        // line comment at last line''')
        self._assert_declaration(m, 'Foo')

    def test_visit_empty_declaration(self):
        m = self.parser.parse_string(r'''
        interface IFoo {
            ;
        }
        class Foo {
            ;
        };''')
        v = Visitor()
        m.accept(v)

    def test_visit_abstract_method(self):
        m = self.parser.parse_string(r'''
        abstract class Foo {
            abstract void foo();
        }
        ''')
        v = Visitor()
        m.accept(v)

    def test_visit_right_hand_this(self):
        m = self.parser.parse_string(r'''
        class Foo {
            static Foo instance;
            Foo() {
                instance = this;
            }
        }
        ''')
        v = Visitor()
        m.accept(v)

    def _assert_declaration(self, compilation_unit, name, index=0,
                            declaration_type=ClassDeclaration):
        self.assertIsInstance(compilation_unit, CompilationUnit)
        self.assertTrue(len(compilation_unit.type_declarations) >= index + 1)

        declaration = compilation_unit.type_declarations[index]
        self.assertIsInstance(declaration, declaration_type)

        self.assertEqual(declaration.name, name)

        return declaration
