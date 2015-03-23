#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, Declaration, Modifier
from plyj.utility import assert_type, assert_none_or, serialize_modifiers


class CompilationUnit(SourceElement):
    package_declaration = property(attrgetter("_package_declaration"))
    import_declarations = property(attrgetter("_import_declarations"))
    type_declarations = property(attrgetter("_type_declarations"))

    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = ['package_declaration', 'import_declarations',
                        'type_declarations']

        self._package_declaration = None
        self._import_declarations = None
        self._type_declarations = None

        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations

    @package_declaration.setter
    def package_declaration(self, package_declaration):
        self._package_declaration = assert_none_or(package_declaration,
                                                   PackageDeclaration)

    @import_declarations.setter
    def import_declarations(self, import_declarations):
        self._import_declarations = self._assert_list(import_declarations,
                                                      ImportDeclaration)

    @type_declarations.setter
    def type_declarations(self, type_declarations):
        self._type_declarations = self._assert_list(type_declarations,
                                                    Declaration)

    def serialize(self):
        retn = ""
        if self.package_declaration is not None:
            retn += self.package_declaration.serialize() + ";\n\n"
        for x in self.import_declarations:
            retn += x.serialize() + ";\n"
        if len(self.import_declarations) > 0:
            retn += "\n"
        for x in self.type_declarations:
            retn += x.serialize() + "\n"
        return retn


class PackageDeclaration(SourceElement):
    name = property(attrgetter("_name"))
    modifiers = property(attrgetter("_modifiers"))

    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']

        self._name = None
        self._modifiers = None

        self.name = name
        self.modifiers = modifiers

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, False)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    def serialize(self):
        modifiers = serialize_modifiers(self.modifiers)
        return modifiers + "package " + self.name.serialize()


class ImportDeclaration(SourceElement):
    name = property(attrgetter("_name"))
    static = property(attrgetter("_static"))
    on_demand = property(attrgetter("_on_demand"))

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']

        self._name = None
        self._static = None
        self._on_demand = None

        self.name = name
        self.static = static
        self.on_demand = on_demand

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, False)

    @static.setter
    def static(self, static):
        self._static = assert_type(static, bool)

    @on_demand.setter
    def on_demand(self, on_demand):
        self._on_demand = assert_type(on_demand, bool)

    def serialize(self):
        static = "static " if self.static else ""
        on_demand = ".*" if self.on_demand else ""
        return "import " + static + self.name.serialize() + on_demand