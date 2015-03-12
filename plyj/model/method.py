#!/usr/bin/env python2
from plyj.model.name import Name, ensure_name, PrimitiveType
from plyj.model.source_element import SourceElement, AnonymousSourceElement, \
    ensure_se
from plyj.model.type import Type, ensure_type
from plyj.model.variable import Variable


class MethodDeclaration(SourceElement):
    def __init__(self, name, modifiers=None, type_parameters=None,
                 parameters=None, return_type='void', body=None,
                 abstract=False,
                 extended_dims=0, throws=None):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'type_parameters', 'parameters',
                        'return_type', 'body', 'abstract', 'extended_dims',
                        'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        if body is None:
            body = []

        return_type = ensure_type(return_type)
        abstract = ensure_se(abstract)
        extended_dims = ensure_se(extended_dims)

        name = ensure_name(name, True)
        assert isinstance(modifiers, list)
        assert isinstance(type_parameters, list)
        assert isinstance(parameters, list)
        assert isinstance(return_type, (Type, PrimitiveType))
        assert isinstance(body, list)
        assert isinstance(abstract, AnonymousSourceElement)
        assert isinstance(extended_dims, AnonymousSourceElement)
        assert throws is None or isinstance(throws, Throws)

        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.abstract = abstract
        self.extended_dims = extended_dims
        self.throws = throws


class FormalParameter(SourceElement):
    def __init__(self, variable, parameter_type, modifiers=None, vararg=None):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']
        if modifiers is None:
            modifiers = []

        parameter_type = ensure_se(parameter_type)
        vararg = ensure_se(vararg)

        assert isinstance(variable, Variable)
        assert isinstance(parameter_type, (Type, AnonymousSourceElement))
        assert isinstance(modifiers, list)
        assert vararg is None or isinstance(vararg, AnonymousSourceElement)

        self.variable = variable
        self.type = parameter_type
        self.modifiers = modifiers
        self.vararg = vararg


class Throws(SourceElement):
    def __init__(self, types):
        super(Throws, self).__init__()
        self._fields = ['types']
        assert isinstance(types, list)
        self.types = types