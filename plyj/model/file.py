#!/usr/bin/env python2
from plyj.model.name import Name, ensure_name
from plyj.model.source_element import SourceElement, ensure_se, \
    AnonymousSourceElement


class CompilationUnit(SourceElement):
    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = [
            'package_declaration', 'import_declarations', 'type_declarations']
        if import_declarations is None:
            import_declarations = []
        if type_declarations is None:
            type_declarations = []

        assert (package_declaration is None or
                isinstance(package_declaration, PackageDeclaration))
        assert isinstance(import_declarations, list)
        assert isinstance(type_declarations, list)

        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations


class ImportDeclaration(SourceElement):
    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']

        name = ensure_name(name, False)
        assert isinstance(static, bool)
        assert isinstance(on_demand, bool)

        self.name = name
        self.static = static
        self.on_demand = on_demand


class PackageDeclaration(SourceElement):
    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']
        if modifiers is None:
            modifiers = []

        name = ensure_name(name, False)
        assert isinstance(modifiers, list)

        self.name = name
        self.modifiers = modifiers