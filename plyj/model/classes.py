#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


class ClassInitializer(SourceElement):
    def __init__(self, block, static=False, tokens=None):
        super(ClassInitializer, self).__init__(tokens)
        self._fields = ['block', 'static']
        self.block = block
        self.static = static


class ClassDeclaration(SourceElement):
    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None, tokens=None):
        super(ClassDeclaration, self).__init__(tokens)
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements']
        self.name = name
        self.body = body
        self.modifiers = modifiers or []
        self.type_parameters = type_parameters or []
        self.extends = extends
        self.implements = implements or []


class ConstructorDeclaration(SourceElement):
    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None, tokens=None):
        super(ConstructorDeclaration, self).__init__(tokens)
        self._fields = ['name', 'block', 'modifiers',
                        'type_parameters', 'parameters', 'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.block = block
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws


class EmptyDeclaration(SourceElement):
    """
    Created for stray semi-colons (;) in class/interface definitions.
    """
    pass


class FieldDeclaration(SourceElement):
    def __init__(self, field_type, variable_declarators,
                 modifiers=None, tokens=None):
        super(FieldDeclaration, self).__init__(tokens)
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = field_type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers


class Wildcard(SourceElement):
    def __init__(self, bounds=None, tokens=None):
        super(Wildcard, self).__init__(tokens)
        self._fields = ['bounds']
        if bounds is None:
            bounds = []
        self.bounds = bounds


class WildcardBound(SourceElement):
    def __init__(self, bound_type, extends=False, _super=False, tokens=None):
        super(WildcardBound, self).__init__(tokens)
        self._fields = ['type', 'extends', '_super']
        self.type = bound_type
        self.extends = extends
        self._super = _super


class TypeParameter(SourceElement):
    """
    Represents a type parameter in the definition of a class.
    """

    def __init__(self, name, extends=None, tokens=None):
        super(TypeParameter, self).__init__(tokens)
        self._fields = ['name', 'extends']
        if extends is None:
            extends = []
        self.name = name
        self.extends = extends