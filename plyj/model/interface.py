#!/usr/bin/env python2
from plyj.model.name import Name, ensure_name
from plyj.model.source_element import SourceElement


class InterfaceDeclaration(SourceElement):
    def __init__(self, name, modifiers=None, extends=None,
                 type_parameters=None,
                 body=None):
        super(InterfaceDeclaration, self).__init__()
        self._fields = [
            'name', 'modifiers', 'extends', 'type_parameters', 'body']
        if modifiers is None:
            modifiers = []
        if extends is None:
            extends = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []

        name = ensure_name(name, True)
        assert isinstance(modifiers, list)
        assert isinstance(extends, list)
        assert isinstance(type_parameters, list)
        assert isinstance(body, list)

        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body