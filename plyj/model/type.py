#!/usr/bin/env python2
from plyj.model.name import Name, ensure_name, is_primitive_type, PrimitiveType
from plyj.model.source_element import SourceElement, AnonymousSourceElement, \
    ensure_se, extract_tokens


class Type(SourceElement):
    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']

        if type_arguments is None:
            type_arguments = []

        # Deal with primitive types passed as a string
        if isinstance(name, str) and is_primitive_type(name):
            name = PrimitiveType(name)

        name = ensure_name(name, False)
        dimensions = ensure_se(dimensions)
        type_arguments = extract_tokens(self, type_arguments)

        # Primitive types (int, byte, etc.) are strings, not names.
        assert enclosed_in is None or isinstance(enclosed_in, Type)
        assert isinstance(type_arguments, list)
        assert isinstance(dimensions, AnonymousSourceElement)

        for x in type_arguments:
            assert isinstance(x, Type)

        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions


def is_primitive_type(type_str):
    return type_str in ["boolean", "void", "byte",
                        "short", "int", "long",
                        "char", "float", "double"]


class PrimitiveType(Type):
    def __init__(self, value):
        super(PrimitiveType, self).__init__(value, True)
        assert is_primitive_type(value)


def ensure_type(type_name):
    if isinstance(type_name, str):
        return Type(type_name)
    if not isinstance(type_name, Type):
        assert False
    return type_name


class TypeParameter(SourceElement):
    """
    Represents a type parameter in the definition of a class.
    """

    def __init__(self, name, extends=None):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends']
        if extends is None:
            extends = []

        name = ensure_name(name, True)
        assert isinstance(extends, list)

        self.name = name
        self.extends = extends