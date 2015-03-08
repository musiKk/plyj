#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


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
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations


class ImportDeclaration(SourceElement):
    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']
        self.name = name
        self.static = static
        self.on_demand = on_demand


class PackageDeclaration(SourceElement):
    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.name = name
        self.modifiers = modifiers