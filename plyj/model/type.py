#!/usr/bin/env python2
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSourceElement, \
    ensure_se, extract_tokens


class Type(SourceElement):
    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']

        if type_arguments is None:
            type_arguments = []

        name = ensure_se(name)
        dimensions = ensure_se(dimensions)
        type_arguments = extract_tokens(self, type_arguments)

        # Primitive types (int, byte, etc.) are strings, not names.
        assert isinstance(name, (Name, AnonymousSourceElement))
        assert enclosed_in is None or isinstance(enclosed_in, Type)
        assert isinstance(type_arguments, list)
        assert isinstance(dimensions, AnonymousSourceElement)

        for x in type_arguments:
            assert isinstance(x, Type)

        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions


class TypeParameter(SourceElement):
    """
    Represents a type parameter in the definition of a class.
    """

    def __init__(self, name, extends=None):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends']
        if extends is None:
            extends = []

        name = ensure_se(name)

        assert (isinstance(name, Name) or
                isinstance(name, AnonymousSourceElement))
        assert isinstance(extends, list)

        self.name = name
        self.extends = extends