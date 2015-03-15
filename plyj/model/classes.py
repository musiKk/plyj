#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.method import FormalParameter, Throws
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, Declaration, Modifier
from plyj.model.statement import Block, VariableDeclaration
from plyj.model.type import Type, TypeParameter
from plyj.utility import assert_type, assert_none_or


class ClassInitializer(Declaration):
    block = property(attrgetter("_block"))
    static = property(attrgetter("_static"))

    def __init__(self, block, static=False):
        super(ClassInitializer, self).__init__()
        self._fields = ['block', 'static']

        self._block = assert_type(block, Block)
        self._static = assert_type(static, bool)


class ClassDeclaration(Declaration):
    name = property(attrgetter("_name"))
    body = property(attrgetter("_body"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    extends = property(attrgetter("_extends"))
    implements = property(attrgetter("_implements"))

    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None):
        super(ClassDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements']

        body = self._absorb_ase_tokens(body)

        self._name = Name.ensure(name, True)
        self._body = self._assert_list(body, Declaration)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._extends = assert_none_or(extends, Type)
        self._implements = self._assert_list(implements, Type)


class ConstructorDeclaration(Declaration):
    name = property(attrgetter("_name"))
    block = property(attrgetter("_block"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    parameters = property(attrgetter("_parameters"))
    throws = property(attrgetter("_throws"))

    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'block', 'modifiers',
                        'type_parameters', 'parameters', 'throws']

        self._name = Name.ensure(name, True)
        self._block = assert_none_or(block, Block)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._parameters = None
        self._throws = None

        self.set_parameters(parameters)
        self.set_throws(throws)

    def set_parameters(self, parameters):
        self._parameters = self._assert_list(parameters, FormalParameter)

    def set_throws(self, throws):
        self._throws = assert_none_or(throws, Throws)


class EmptyDeclaration(Declaration):
    """
    Created for stray semi-colons (;) in class/interface definitions.
    """
    pass


class FieldDeclaration(VariableDeclaration):
    pass


class WildcardBound(SourceElement):
    type = property(attrgetter("_type"))
    extends = property(attrgetter("_extends"))
    super = property(attrgetter("_super"))

    def __init__(self, type_, extends=False, super_=False):
        super(WildcardBound, self).__init__()
        self._fields = ['type', 'extends', 'super']

        self._type = Type.ensure(type_)
        self._extends = assert_type(extends, bool)
        self._super = assert_none_or(super_, bool)


class Wildcard(SourceElement):
    bounds = property(attrgetter("_bounds"))

    def __init__(self, bounds=None):
        super(Wildcard, self).__init__()
        self._fields = ['bounds']

        self._bounds = self._assert_list(bounds, WildcardBound)