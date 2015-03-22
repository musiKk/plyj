#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.method import FormalParameter, Throws
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, Declaration, Modifier
from plyj.model.statement import Block, VariableDeclaration
from plyj.model.type import Type, TypeParameter
from plyj.utility import assert_type, assert_none_or, serialize_type_parameters, \
    serialize_extends, serialize_implements, serialize_body, \
    serialize_parameters, serialize_modifiers


class ClassInitializer(Declaration):
    block = property(attrgetter("_block"))
    static = property(attrgetter("_static"))

    def __init__(self, block, static=False):
        super(ClassInitializer, self).__init__()
        self._fields = ['block', 'static']

        self._block = None
        self._static = None

        self.block = block
        self.static = static

    @block.setter
    def block(self, block):
        self._block = assert_type(block, Block)

    @static.setter
    def static(self, static):
        self._static = assert_type(static, bool)

    def serialize(self):
        return ("static " if self.static else "") + self.block.serialize()


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

        self._name = None
        self._body = None
        self._modifiers = None
        self._type_parameters = None
        self._extends = None
        self._implements = None

        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @body.setter
    def body(self, body):
        body = self._alter_tokens("body", body)
        self._body = self._assert_list(body, Declaration)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @type_parameters.setter
    def type_parameters(self, type_parameters):
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)

    @extends.setter
    def extends(self, extends):
        self._extends = assert_none_or(extends, Type)

    @implements.setter
    def implements(self, implements):
        self._implements = self._assert_list(implements, Type)

    def serialize(self):
        return "{}class {}{} {}{}{}".format(
            serialize_modifiers(self.modifiers),
            self.name.serialize(),
            serialize_type_parameters(self.type_parameters),
            serialize_extends(self.extends),
            serialize_implements(self.implements),
            serialize_body(self.body)
        )


class ConstructorDeclaration(Declaration):
    name = property(attrgetter("_name"))
    body = property(attrgetter("_body"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    parameters = property(attrgetter("_parameters"))
    throws = property(attrgetter("_throws"))

    def __init__(self, name, body=None, modifiers=None, type_parameters=None,
                 parameters=None, throws=None):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'parameters', 'throws']

        self._name = None
        self._body = None
        self._modifiers = None
        self._type_parameters = None
        self._parameters = None
        self._throws = None

        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @body.setter
    def body(self, body):
        self._body = self._assert_body(body)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @type_parameters.setter
    def type_parameters(self, type_parameters):
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = self._assert_list(parameters, FormalParameter)

    @throws.setter
    def throws(self, throws):
        self._throws = assert_none_or(throws, Throws)

    def serialize(self):
        type_parameters = serialize_type_parameters(self.type_parameters)
        if len(type_parameters) > 0:
            type_parameters += " "
        return "{}{}{}{}{} {}".format(
            serialize_modifiers(self.modifiers),
            type_parameters,
            self.name.serialize(),
            serialize_parameters(self.parameters),
            "" if self.throws is None else self.throws.serialize(),
            serialize_body(self.body)
        )


class EmptyDeclaration(Declaration):
    """
    Created for stray semi-colons (;) in class/interface definitions.
    """
    def serialize(self):
        return ";"


class FieldDeclaration(VariableDeclaration):
    pass


class WildcardBound(SourceElement):
    type = property(attrgetter("_type"))
    extends = property(attrgetter("_extends"))
    super = property(attrgetter("_super"))

    def __init__(self, type_, extends=False, super_=False):
        super(WildcardBound, self).__init__()
        self._fields = ['type', 'extends', 'super']

        self._type = None
        self._extends = False
        self._super = False

        self.type = type_
        self.extends = extends
        self.super = super_

    @type.setter
    def type(self, type_):
        self._type = Type.ensure(type_)

    @extends.setter
    def extends(self, extends):
        self._extends = assert_type(extends, bool)
        assert not (self.super and self.extends)

    @super.setter
    def super(self, super_):
        self._super = assert_type(super_, bool)
        assert not (self.super and self.extends)

    def serialize(self):
        if self.extends:
            keywords = "extends "
        elif self.super:
            keywords = "super "
        else:
            keywords = ""
        return "{}{}".format(
            keywords,
            self.type.serialize()
        )


class Wildcard(SourceElement):
    bounds = property(attrgetter("_bounds"))

    def __init__(self, bounds=None):
        super(Wildcard, self).__init__()
        self._fields = ['bounds']

        self._bounds = None

        self.bounds = bounds

    @bounds.setter
    def bounds(self, bounds):
        self._bounds = self._assert_list(bounds, WildcardBound)

    def serialize(self):
        return "?{}".format(
            "".join([" " + x.serialize() for x in self.bounds])
        )