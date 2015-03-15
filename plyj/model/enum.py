#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.method import FormalParameter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, Declaration, Statement, \
    Modifier, Expression
from plyj.model.type import Type, TypeParameter


class EnumDeclaration(Declaration):
    name = property(attrgetter("_name"))
    implements = property(attrgetter("_implements"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    body = property(attrgetter("_body"))

    def __init__(self, name, implements=None, modifiers=None,
                 type_parameters=None, body=None):
        super(EnumDeclaration, self).__init__()
        self._fields = ['name', 'implements', 'modifiers', 'type_parameters',
                        'body']

        body = self._absorb_ase_tokens(body)

        self._name = Name.ensure(name, True)
        self._implements = self._assert_list(implements, Type)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._body = self._assert_list(body, (EnumConstant, Declaration))


class EnumConstant(SourceElement):
    name = property(attrgetter("_name"))
    arguments = property(attrgetter("_arguments"))
    modifiers = property(attrgetter("_modifiers"))
    body = property(attrgetter("_body"))

    def __init__(self, name, arguments=None, modifiers=None, body=None):
        super(EnumConstant, self).__init__()
        self._fields = ['name', 'arguments', 'modifiers', 'body']

        self._name = Name.ensure(name, True)
        self._arguments = self._assert_list(arguments, Expression)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._body = self._assert_list(body, Declaration)