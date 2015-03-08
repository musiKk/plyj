#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


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
    def __init__(self, variable, parameter_type, modifiers=None, vararg=False):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = parameter_type
        self.modifiers = modifiers
        self.vararg = vararg


class Throws(SourceElement):
    def __init__(self, types):
        super(Throws, self).__init__()
        self._fields = ['types']
        self.types = types