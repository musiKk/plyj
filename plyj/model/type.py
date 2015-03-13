#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE


class Type(SourceElement):
    name = property(attrgetter("_name"))
    type_arguments = property(attrgetter("_type_arguments"))
    enclosed_in = property(attrgetter("_enclosed_in"))
    dimensions = property(attrgetter("_dimensions"))

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']

        if type_arguments is None:
            type_arguments = []

        type_arguments = self._absorb_ase_tokens(type_arguments)
        name = Name.ensure(name, False)

        # Primitive types (int, byte, etc.) are strings, not names.
        assert isinstance(type_arguments, list)

        for x in type_arguments:
            assert isinstance(x, Type)

        self._name = name
        self._type_arguments = type_arguments
        self._dimensions = None
        self._enclosed_in = None

        self.set_enclosed_in(enclosed_in)
        self.set_dimensions(dimensions)

    def set_enclosed_in(self, enclosed_in):
        assert enclosed_in is None or isinstance(enclosed_in, Type)
        self._enclosed_in = enclosed_in

    def set_dimensions(self, dimensions):
        dimensions = AnonymousSE.ensure(dimensions)
        assert isinstance(dimensions, AnonymousSE)
        self._dimensions = dimensions

    @staticmethod
    def ensure(type_name):
        if isinstance(type_name, str):
            return Type(type_name)
        if not isinstance(type_name, Type):
            assert False
        return type_name

    @staticmethod
    def is_primitive(type_):
        if isinstance(type_, Type):
            type_ = type_.name
        assert isinstance(type_, (str, unicode))
        return type_ in ["boolean", "void", "byte", "short", "int", "long",
                         "char", "float", "double"]


class TypeParameter(SourceElement):
    """
    Represents a type parameter in the definition of a class.
    """

    def __init__(self, name, extends=None):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends']
        if extends is None:
            extends = []

        name = Name.ensure(name, True)
        assert isinstance(extends, list)

        self.name = name
        self.extends = extends