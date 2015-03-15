#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Expression, \
    Statement, Modifier
from plyj.model.type import Type, TypeParameter
from plyj.utility import assert_none_or, assert_type


class Annotation(Modifier):
    name = property(attrgetter("_name"))
    members = property(attrgetter("_members"))
    single_member = property(attrgetter("_single_member"))

    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member']

        members = self._absorb_ase_tokens(members)

        self._name = Name.ensure(name, True)
        self._members = self._assert_list(members, AnnotationMember)
        self._single_member = assert_none_or(single_member, AnnotationMember)


class AnnotationMethodDeclaration(SourceElement):
    name = property(attrgetter("_name"))
    type = property(attrgetter("_type"))
    parameters = property(attrgetter("_parameters"))
    default = property(attrgetter("_default"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    extended_dims = property(attrgetter("_extended_dims"))

    def __init__(self, name, return_type, parameters=None, default=None,
                 modifiers=None, type_parameters=None, extended_dims=0):
        super(AnnotationMethodDeclaration, self).__init__()
        self._fields = ['name', 'type', 'parameters', 'default',
                        'modifiers', 'type_parameters', 'extended_dims']

        self._name = Name.ensure(name, True)
        self._type = assert_type(return_type, Type)
        self._parameters = self._assert_list(parameters, Expression)
        self._default = assert_none_or(default, Expression)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._extended_dims = AnonymousSE.ensure(extended_dims)


class AnnotationMember(SourceElement):
    name = property(attrgetter("_name"))
    value = property(attrgetter("_value"))

    def __init__(self, name, value):
        super(AnnotationMember, self).__init__()
        self._fields = ['name', 'value']

        self._name = Name.ensure(name, True)
        self._value = assert_type(value, Expression)


class AnnotationDeclaration(SourceElement):
    name = property(attrgetter("_name"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    extends = property(attrgetter("_extends"))
    implements = property(attrgetter("_implements"))
    body = property(attrgetter("_body"))

    def __init__(self, name, modifiers=None, type_parameters=None,
                 extends=None, implements=None, body=None):
        super(AnnotationDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'type_parameters', 'extends',
                        'implements', 'body']

        self._name = Name.ensure(name, True)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._extends = assert_none_or(extends, Type)
        self._implements = self._assert_list(implements, TypeParameter)
        self._body = self._assert_list(body, Statement)