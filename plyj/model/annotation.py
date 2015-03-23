#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.expression import ArrayInitializer
from plyj.model.method import FormalParameter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Expression, \
    Modifier, Declaration
from plyj.model.type import Type, TypeParameter
from plyj.utility import assert_none_or, assert_type, \
    serialize_type_parameters, serialize_extends, serialize_implements, \
    serialize_body, serialize_modifiers


class Annotation(Modifier):
    """
    An Annotation is serialized to the following:

    If there are no members:
        @<name>
    If there is a single_member:
        @<name>(<single_member>)
    If there are members (implies no single member):
        @<name>(<members separated by commas>)
    """
    name = property(attrgetter("_name"))
    members = property(attrgetter("_members"))
    single_member = property(attrgetter("_single_member"))

    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member']

        self._name = None
        self._members = None
        self._single_member = None

        self.name = name
        self.members = members
        self.single_member = single_member

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, False)

    @members.setter
    def members(self, members):
        members = self._alter_tokens("members", members)
        assert (members is None or len(members) == 0
                or self.single_member is None)
        self._members = self._assert_list(members, AnnotationMember)

    @single_member.setter
    def single_member(self, single_member):
        assert single_member is None or len(self.members) == 0
        self._single_member = assert_none_or(single_member, MEMBER_VALUE_TYPES)

    def serialize(self):
        if len(self.members) == 0:
            if self.single_member is None:
                return "@" + self.name.serialize()
            else:
                return "@{}({})".format(self.name.serialize(),
                                        self.single_member.serialize())
        else:
            assert self.single_member is None
            members = ", ".join([x.serialize() for x in self.members])
            return "@{}({})".format(self.name.serialize(), members)


MEMBER_VALUE_TYPES = (Annotation, Expression, ArrayInitializer)


class AnnotationMethodDeclaration(Declaration):
    name = property(attrgetter("_name"))
    return_type = property(attrgetter("_return_type"))
    parameters = property(attrgetter("_parameters"))
    default = property(attrgetter("_default"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    extended_dims = property(attrgetter("_extended_dims"))

    def __init__(self, name, return_type, parameters=None, default=None,
                 modifiers=None, type_parameters=None, extended_dims=0):
        super(AnnotationMethodDeclaration, self).__init__()
        self._fields = ['name', 'return_type', 'parameters', 'default',
                        'modifiers', 'type_parameters', 'extended_dims']

        self._name = None
        self._return_type = None
        self._parameters = None
        self._default = None
        self._modifiers = None
        self._type_parameters = None
        self._extended_dims = None

        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @return_type.setter
    def return_type(self, return_type):
        self._return_type = assert_type(return_type, Type)

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = self._assert_list(parameters, FormalParameter)

    @default.setter
    def default(self, default):
        self._default = assert_none_or(default, MEMBER_VALUE_TYPES)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @type_parameters.setter
    def type_parameters(self, type_parameters):
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)

    @extended_dims.setter
    def extended_dims(self, extended_dims):
        self._extended_dims = AnonymousSE.ensure(extended_dims)
        assert_type(self._extended_dims.value, int)

    def serialize(self):
        type_parameters = serialize_type_parameters(self.type_parameters)
        dimensions = "[]" * self.extended_dims.value
        default = ""
        if self.default is not None:
            default = " default " + self.default.serialize()
        if len(type_parameters) > 0:
            type_parameters += " "
        return "{}{}{} {}({}){}{};".format(
            serialize_modifiers(self.modifiers),
            type_parameters,
            self.return_type.serialize(),
            self.name.serialize(),
            ", ".join([x.serialize() for x in self.parameters]),
            dimensions,
            default)


class AnnotationMember(SourceElement):
    name = property(attrgetter("_name"))
    value = property(attrgetter("_value"))

    def __init__(self, name, value):
        super(AnnotationMember, self).__init__()
        self._fields = ['name', 'value']

        self._name = None
        self._value = None

        self.name = name
        self.value = value

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @value.setter
    def value(self, value):
        self._value = assert_type(value, MEMBER_VALUE_TYPES)

    def serialize(self):
        return self.name.serialize() + "=" + self.value.serialize()


class AnnotationDeclaration(Declaration):
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

        self._name = None
        self._modifiers = None
        self._type_parameters = None
        self._extends = None
        self._implements = None
        self._body = None

        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

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
        self._implements = self._assert_list(implements, TypeParameter)

    @body.setter
    def body(self, body):
        self._body = self._assert_list(body, Declaration)

    def serialize(self):
        return "{}@interface {}{} {}{}{}".format(
            serialize_modifiers(self.modifiers),
            self.name.serialize(),
            serialize_type_parameters(self.type_parameters),
            serialize_extends(self.extends),
            serialize_implements(self.implements),
            serialize_body(self.body)
        )