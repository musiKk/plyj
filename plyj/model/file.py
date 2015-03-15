#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, Declaration, Modifier
from plyj.utility import assert_type, assert_none_or


class CompilationUnit(SourceElement):
    package_declaration = property(attrgetter("_package_declaration"))
    import_declarations = property(attrgetter("_import_declarations"))
    type_declarations = property(attrgetter("_type_declarations"))

    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = ['package_declaration', 'import_declarations',
                        'type_declarations']

        self._package_declaration = assert_none_or(package_declaration,
                                                   PackageDeclaration)
        self._import_declarations = self._assert_list(import_declarations,
                                                      ImportDeclaration)
        self._type_declarations = self._assert_list(type_declarations,
                                                    Declaration)


class PackageDeclaration(SourceElement):
    name = property(attrgetter("_name"))
    modifiers = property(attrgetter("_modifiers"))

    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']

        self._name = Name.ensure(name, False)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)


class ImportDeclaration(SourceElement):
    name = property(attrgetter("_name"))
    static = property(attrgetter("_static"))
    on_demand = property(attrgetter("_on_demand"))

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']

        self._name = Name.ensure(name, False)
        self._static = assert_type(static, bool)
        self._on_demand = assert_type(on_demand, bool)