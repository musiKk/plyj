#!/usr/bin/env python2
from plyj.model.name import Name, ensure_name
from plyj.model.source_element import SourceElement, ensure_se, \
    AnonymousSourceElement


class EnumDeclaration(SourceElement):
    def __init__(self, name, implements=None, modifiers=None,
                 type_parameters=None, body=None):
        super(EnumDeclaration, self).__init__()
        self._fields = [
            'name', 'implements', 'modifiers', 'type_parameters', 'body']
        if implements is None:
            implements = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []

        name = ensure_name(name, True)
        assert isinstance(implements, list)
        assert isinstance(modifiers, list)
        assert isinstance(type_parameters, list)
        assert isinstance(body, list)

        self.name = name
        self.implements = implements
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.body = body


class EnumConstant(SourceElement):
    def __init__(self, name, arguments=None, modifiers=None, body=None):
        super(EnumConstant, self).__init__()
        self._fields = ['name', 'arguments', 'modifiers', 'body']
        if arguments is None:
            arguments = []
        if modifiers is None:
            modifiers = []
        if body is None:
            body = []

        name = ensure_name(name, True)
        assert isinstance(arguments, list)
        assert isinstance(modifiers, list)
        assert isinstance(body, list)

        self.name = name
        self.arguments = arguments
        self.modifiers = modifiers
        self.body = body