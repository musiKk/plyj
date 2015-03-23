#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, \
    Declaration, Modifier
from plyj.model.type import Type, TypeParameter
from plyj.model.variable import Variable
from plyj.utility import assert_type, assert_none_or, \
    serialize_type_parameters, serialize_body, serialize_modifiers


class MethodDeclaration(Declaration):
    name = property(attrgetter("_name"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    parameters = property(attrgetter("_parameters"))
    return_type = property(attrgetter("_return_type"))
    body = property(attrgetter("_body"))
    abstract = property(attrgetter("_abstract"))
    extended_dims = property(attrgetter("_extended_dims"))
    throws = property(attrgetter("_throws"))

    def __init__(self, name, modifiers=None, type_parameters=None,
                 parameters=None, return_type='void', body=None,
                 abstract=False, extended_dims=0, throws=None):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'type_parameters', 'parameters',
                        'return_type', 'body', 'abstract', 'extended_dims',
                        'throws']

        self._name = None
        self._modifiers = None
        self._type_parameters = None
        self._parameters = None
        self._return_type = None
        self._body = None
        self._abstract = None
        self._extended_dims = None
        self._throws = None

        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.abstract = abstract
        self.extended_dims = extended_dims
        self.throws = throws

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

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = self._assert_list(parameters, FormalParameter)

    @return_type.setter
    def return_type(self, return_type):
        self._return_type = Type.ensure(return_type)

    @body.setter
    def body(self, body):
        self._body = self._assert_body(body)

    @abstract.setter
    def abstract(self, abstract):
        self._abstract = AnonymousSE.ensure(abstract)

    @extended_dims.setter
    def extended_dims(self, extended_dims):
        self._extended_dims = AnonymousSE.ensure(extended_dims)

    @throws.setter
    def throws(self, throws):
        self._throws = assert_none_or(throws, Throws)

    def serialize(self):
        type_parameters = serialize_type_parameters(self.type_parameters)
        if len(type_parameters) > 0:
            type_parameters += " "
        dimensions = "[]" * self.extended_dims.value
        throws = "" if self.throws is None else self.throws.serialize()
        return "{}{}{} {}({}){}{}{}{}".format(
            serialize_modifiers(self.modifiers),
            type_parameters,
            self.return_type.serialize(),
            self.name.serialize(),
            ", ".join([x.serialize() for x in self.parameters]),
            dimensions,
            # Add a space before throws/body if we have either
            " " if self.throws is not None or not self.abstract.value else "",
            throws,
            ";" if self.abstract.value else serialize_body(self.body))


class FormalParameter(SourceElement):
    variable = property(attrgetter("_variable"))
    type = property(attrgetter("_type"))
    modifiers = property(attrgetter("_modifiers"))
    vararg = property(attrgetter("_vararg"))

    def __init__(self, variable, type_, modifiers=None, vararg=None):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']

        self._variable = None
        self._type = None
        self._modifiers = None
        self._vararg = None

        self.variable = variable
        self.type = type_
        self.modifiers = modifiers
        self.vararg = vararg

    @variable.setter
    def variable(self, variable):
        self._variable = assert_type(variable, Variable)

    @type.setter
    def type(self, type_):
        self._type = Type.ensure(type_)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @vararg.setter
    def vararg(self, vararg):
        self._vararg = AnonymousSE.ensure(vararg)

    def serialize(self):
        return "{}{}{} {}".format(
            serialize_modifiers(self.modifiers),
            self.type.serialize(),
            " ..." if self.vararg.value else "",
            self.variable.serialize())


class Throws(SourceElement):
    types = property(attrgetter("_types"))

    def __init__(self, types):
        super(Throws, self).__init__()
        self._fields = ['types']

        self._types = None

        self.types = types

    @types.setter
    def types(self, types):
        self._types = self._assert_list_ensure(types, Type)

    def serialize(self):
        return "throws " + ", ".join([x.serialize() for x in self.types])