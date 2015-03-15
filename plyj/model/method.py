#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Statement, \
    Declaration, Modifier
from plyj.model.type import Type, TypeParameter
from plyj.model.variable import Variable
from plyj.utility import assert_type, assert_none_or


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

        self._name = Name.ensure(name, True)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)
        self._parameters = self._assert_list(parameters, FormalParameter)
        self._return_type = Type.ensure(return_type)
        self._body = self._assert_body(body)
        self._abstract = AnonymousSE.ensure(abstract)
        self._extended_dims = AnonymousSE.ensure(extended_dims)
        self._throws = assert_none_or(throws, Throws)


class FormalParameter(SourceElement):
    variable = property(attrgetter("_variable"))
    parameter_type = property(attrgetter("_parameter_type"))
    modifiers = property(attrgetter("_modifiers"))
    vararg = property(attrgetter("_vararg"))

    def __init__(self, variable, parameter_type, modifiers=None, vararg=None):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']

        self._variable = assert_type(variable, Variable)
        self._parameter_type = Type.ensure(parameter_type)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._vararg = AnonymousSE.ensure(vararg)


class Throws(SourceElement):
    types = property(attrgetter("_types"))

    def __init__(self, types):
        super(Throws, self).__init__()
        self._fields = ['types']

        self._types = self._assert_list_ensure(types, Type)