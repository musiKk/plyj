import unittest

import plyj.parser as plyj
import plyj.model as model

class CompilationUnitTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

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
        self.assertEqual(m.package_declaration, model.PackageDeclaration(model.Name('foo.bar')))

    def test_package_annotation(self):
        m = self.parser.parse_string('''
        @Annot
        package foo;
        ''')
        self.assertEqual(m.package_declaration,
                         model.PackageDeclaration(model.Name('foo'),
                                                  modifiers=[model.Annotation(model.Name('Annot'))]))

    def test_import(self):
        m = self.parser.parse_string('''
        import foo;
        import foo.bar;
        ''')
        self.assertEqual(m.import_declarations,
                         [model.ImportDeclaration(model.Name('foo')),
                          model.ImportDeclaration(model.Name('foo.bar'))])

    def test_static_import(self):
        m = self.parser.parse_string('''
        import static foo.bar;
        ''')
        self.assertEqual(m.import_declarations,
                         [model.ImportDeclaration(model.Name('foo.bar'), static=True)])

    def test_wildcard_import(self):
        m = self.parser.parse_string('''
        import foo.bar.*;
        ''')
        self.assertEqual(m.import_declarations,
                         [model.ImportDeclaration(model.Name('foo.bar'), on_demand=True)])

    def test_static_wildcard_import(self):
        m = self.parser.parse_string('''
        import static foo.bar.*;
        ''')
        self.assertEqual(m.import_declarations,
                         [model.ImportDeclaration(model.Name('foo.bar'), static=True, on_demand=True)])

    def test_annotations(self):
        # bug #13
        m = self.parser.parse_string('''
        @Annot(key = 1)
        class Foo {}
        ''')
        t = self._assert_declaration(m, 'Foo')

        self.assertEqual(t.modifiers, [model.Annotation(
            name=model.Name('Annot'),
            members=[model.AnnotationMember(name=model.Name('key'),
                                            value=model.Literal('1'))])])

    def test_line_comment(self):
        m = self.parser.parse_string(r'''
        class Foo {}
        //
        //\
        // line comment at last line''');
        self._assert_declaration(m, 'Foo')

    def test_visit_empty_declaration(self):
        m = self.parser.parse_string(r'''
        interface IFoo {
            ;
        }
        class Foo {
            ;
        };''')
        v = model.Visitor()
        m.accept(v)

    def test_visit_abstract_method(self):
        m = self.parser.parse_string(r'''
        abstract class Foo {
            abstract void foo();
        }
        ''')
        v = model.Visitor()
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
        v = model.Visitor()
        m.accept(v)

    def _assert_declaration(self, compilation_unit, name, index=0, type=model.ClassDeclaration):
        self.assertIsInstance(compilation_unit, model.CompilationUnit)
        self.assertTrue(len(compilation_unit.type_declarations) >= index + 1)

        decl = compilation_unit.type_declarations[index]
        self.assertIsInstance(decl, type)

        self.assertEqual(decl.name, name)

        return decl
