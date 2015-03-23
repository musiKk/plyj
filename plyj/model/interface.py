#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import Declaration, Modifier
from plyj.model.type import Type, TypeParameter
from plyj.utility import serialize_type_parameters, serialize_body, \
    serialize_extends, serialize_modifiers


class InterfaceDeclaration(Declaration):
    name = property(attrgetter("_name"))
    modifiers = property(attrgetter("_modifiers"))
    extends = property(attrgetter("_extends"))
    type_parameters = property(attrgetter("_type_parameters"))
    body = property(attrgetter("_body"))

    def __init__(self, name, modifiers=None, extends=None,
                 type_parameters=None, body=None):
        super(InterfaceDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'extends', 'type_parameters',
                        'body']

        self._name = None
        self._modifiers = None
        self._extends = None
        self._type_parameters = None
        self._body = None

        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @extends.setter
    def extends(self, extends):
        # Deal with people who put a string literal as the extends parameter.
        if isinstance(extends, str):
            extends = [Type(extends)]
        extends = self._alter_tokens("extends", extends)
        self._extends = self._assert_list_ensure(extends, Type)

    @type_parameters.setter
    def type_parameters(self, type_parameters):
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)

    @body.setter
    def body(self, body):
        body = self._alter_tokens("body", body)
        self._body = self._assert_list(body, Declaration)

    def serialize(self):
        return "{}interface {}{} {}{}".format(
            serialize_modifiers(self.modifiers),
            self.name.serialize(),
            serialize_type_parameters(self.type_parameters),
            serialize_extends(self.extends),
            serialize_body(self.body)
        )