#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import Declaration, Modifier
from plyj.model.type import Type, TypeParameter
from plyj.utility import serialize_type_parameters, serialize_body, \
    serialize_extends


class InterfaceDeclaration(Declaration):
    name = property(attrgetter("_name"))
    modifiers = property(attrgetter("_modifiers"))
    extends = property(attrgetter("_extends"))
    type_parameters = property(attrgetter("_type_parameters"))
    body = property(attrgetter("_body"))

    def serialize(self):
        return "{}interface {}{} {}{}".format(
            "".join([x.serialize() + " " for x in self.modifiers]),
            self.name.serialize(),
            serialize_type_parameters(self.type_parameters),
            serialize_extends(self.extends),
            serialize_body(self.body)
        )

    def __init__(self, name, modifiers=None, extends=None,
                 type_parameters=None, body=None):
        super(InterfaceDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'extends', 'type_parameters',
                        'body']

        # Deal with people who put a string literal as the extends parameter.
        if isinstance(extends, str):
            extends = [Type(extends)]

        extends = self._absorb_ase_tokens(extends)
        body = self._absorb_ase_tokens(body)

        self._name = Name.ensure(name, True)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._extends = self._assert_list_ensure(extends, Type)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._body = self._assert_list(body, Declaration)