#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


class Type(SourceElement):
    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0, tokens=None):
        super(Type, self).__init__(None)
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions
        self.tokens = tokens or []