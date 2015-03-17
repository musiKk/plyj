#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.expression import ArrayInitializer
from plyj.model.method import FormalParameter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Expression, \
    Modifier, Declaration
from plyj.model.type import Type, TypeParameter
from plyj.utility import assert_none_or, assert_type, serialize_type_parameters, serialize_extends, serialize_implements, \
    serialize_body, serialize_modifiers


class Annotation(Modifier):
    name = property(attrgetter("_name"))
    members = property(attrgetter("_members"))
    single_member = property(attrgetter("_single_member"))

    def serialize(self):
        if self.members is None:
            if self.single_member is None:
                return "@" + self.name
            else:
                return "@{}({})".format(self.name,
                                        self.single_member.serialize())
        else:
            assert self.single_member is None
            members = ",".join([x.serialize() for x in self.members])
            return "@{}({})".format(self.name, members)

    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member']

        members = self._absorb_ase_tokens(members)

        if single_member is not None:
            assert members is None

        self._name = Name.ensure(name, False)
        self._members = self._assert_list(members, AnnotationMember)
        self._single_member = assert_none_or(single_member, MEMBER_VALUE_TYPES)

MEMBER_VALUE_TYPES = (Annotation, Expression, ArrayInitializer)


class AnnotationMethodDeclaration(Declaration):
    name = property(attrgetter("_name"))
    type = property(attrgetter("_type"))
    parameters = property(attrgetter("_parameters"))
    default = property(attrgetter("_default"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    extended_dims = property(attrgetter("_extended_dims"))

    def serialize(self):
        """
        annotation_method_header_name
        formal_parameter_list_opt
        ')'
        method_header_extended_dims
        annotation_method_header_default_value_opt
        """
        type_parameters = serialize_type_parameters(self.type_parameters)
        dimensions = "[]" * self.extended_dims.value
        default = "" if self.default is None else " default " + self.default.serialize()
        return "{} {} {}{}({}){}{}".format(
            serialize_modifiers(self.modifiers),
            self.type.serialize(),
            self.name.serialize(),
            type_parameters,
            ", ".join([x.serialize() for x in self.parameters]),
            dimensions,
            default)

    def __init__(self, name, return_type, parameters=None, default=None,
                 modifiers=None, type_parameters=None, extended_dims=0):
        super(AnnotationMethodDeclaration, self).__init__()
        self._fields = ['name', 'type', 'parameters', 'default',
                        'modifiers', 'type_parameters', 'extended_dims']

        self._name = Name.ensure(name, True)
        self._type = assert_type(return_type, Type)
        self._parameters = self._assert_list(parameters, FormalParameter)
        self._default = assert_none_or(default, MEMBER_VALUE_TYPES)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._extended_dims = AnonymousSE.ensure(extended_dims)
        assert_type(self._extended_dims.value, int)


class AnnotationMember(SourceElement):
    name = property(attrgetter("_name"))
    value = property(attrgetter("_value"))

    def serialize(self):
        return self.name.serialize() + "=" + self.value.serialize()

    def __init__(self, name, value):
        super(AnnotationMember, self).__init__()
        self._fields = ['name', 'value']

        self._name = Name.ensure(name, True)
        self._value = assert_type(value, MEMBER_VALUE_TYPES)


class AnnotationDeclaration(Declaration):
    name = property(attrgetter("_name"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    extends = property(attrgetter("_extends"))
    implements = property(attrgetter("_implements"))
    body = property(attrgetter("_body"))

    def serialize(self):
        return "{}@interface {}{}{}{}{}".format(
            serialize_modifiers(self.modifiers),
            self.name.serialize(),
            serialize_type_parameters(self.type_parameters),
            serialize_extends(self.extends),
            serialize_implements(self.implements),
            serialize_body(self.body)
        )

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
        self._body = self._assert_list(body, Declaration)