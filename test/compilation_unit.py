import unittest

import plyj.parser as plyj
import plyj.model as model

class CompilationUnitTest(unittest.TestCase):

    def setUp(self):
        self.parser = plyj.Parser()

    def testAnnotations(self):
        # bug #13
        m = self.parser.parse_string('''
        @Annot(key = 1)
        class Foo {}
        ''')
        self.assertIsInstance(m, model.CompilationUnit)
        self.assertEqual(len(m.type_declarations), 1)

        t = m.type_declarations[0]
        self.assertEqual(len(t.modifiers), 1)

        annot = t.modifiers[0]
        self.assertIsInstance(annot, model.Annotation)

        self.assertEqual(len(annot.members), 1)
        member = annot.members[0]

        self.assertIsInstance(member, model.AnnotationMember)

        self.assertEquals(member, model.AnnotationMember(
            name=model.Name('key'),
            value=model.Literal('1')))
