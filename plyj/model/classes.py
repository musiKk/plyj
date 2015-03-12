#!/usr/bin/env python2
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Statement
from plyj.model.statement import Block, VariableDeclaration
from plyj.model.type import Type


class ClassInitializer(SourceElement):
    def __init__(self, block, static=False):
        super(ClassInitializer, self).__init__()
        self._fields = ['block', 'static']

        assert isinstance(static, bool)
        assert isinstance(block, Block)

        self.block = block
        self.static = static


class ClassDeclaration(SourceElement):
    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None):
        super(ClassDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements']

        implements = [] if implements is None else implements
        modifiers = [] if modifiers is None else modifiers
        type_parameters = [] if type_parameters is None else type_parameters

        name = Name.ensure(name, True)
        body = AnonymousSE.ensure(body)

        assert isinstance(body, AnonymousSE)
        assert isinstance(modifiers, list)
        assert isinstance(type_parameters, list)
        assert extends is None or isinstance(extends, Type)
        assert isinstance(implements, list)

        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements


class ConstructorDeclaration(SourceElement):
    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'block', 'modifiers',
                        'type_parameters', 'parameters', 'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []

        name = Name.ensure(name, True)
        assert block is None or isinstance(block, Block)
        assert isinstance(modifiers, list)
        assert isinstance(type_parameters, list)
        assert isinstance(parameters, list)
        assert throws is None or isinstance(throws, SourceElement)

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


class FieldDeclaration(VariableDeclaration):
    pass


class Wildcard(SourceElement):
    def __init__(self, bounds=None):
        super(Wildcard, self).__init__()
        self._fields = ['bounds']
        if bounds is None:
            bounds = []
        assert isinstance(bounds, list)
        self.bounds = bounds


class WildcardBound(SourceElement):
    def __init__(self, bound_type, extends=False, _super=False):
        super(WildcardBound, self).__init__()
        self._fields = ['type', 'extends', '_super']

        assert isinstance(bound_type, Type)
        assert isinstance(extends, list)
        assert isinstance(_super, bool)

        self.type = bound_type
        self.extends = extends
        self._super = _super


