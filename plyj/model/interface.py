#!/usr/bin/env python2
from plyj.model.classes import FieldDeclaration, EmptyDeclaration, \
    ConstructorDeclaration
from plyj.model.method import MethodDeclaration
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Statement
from plyj.model.type import Type, TypeParameter
from plyj.utility import map_inplace, assert_list


class InterfaceDeclaration(SourceElement):
    def __init__(self, name, modifiers=None, extends=None,
                 type_parameters=None, body=None):
        super(InterfaceDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'extends', 'type_parameters',
                        'body']
        if modifiers is None:
            modifiers = []
        if extends is None:
            extends = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []

        # Deal with people who put a string literal as the extends parameter.
        if isinstance(extends, str):
            extends = [Type(extends)]

        extends = self._absorb_ase_tokens(extends)
        body = self._absorb_ase_tokens(body)
        name = Name.ensure(name, True)
        map_inplace(Type.ensure, extends)
        map_inplace(AnonymousSE.ensure, modifiers)
        assert_list(type_parameters, TypeParameter)
        assert_list(body, (FieldDeclaration, MethodDeclaration,
                           EmptyDeclaration, ConstructorDeclaration))

        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body