#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE
from plyj.utility import assert_none_or_ensure


class Type(SourceElement):
    name = property(attrgetter("_name"))
    type_arguments = property(attrgetter("_type_arguments"))
    enclosed_in = property(attrgetter("_enclosed_in"))
    dimensions = property(attrgetter("_dimensions"))

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']

        self._name = Name.ensure(name, False)
        self._type_arguments = None
        self._type_arguments_tokens = []
        self._dimensions = None
        self._enclosed_in = None

        self.set_enclosed_in(enclosed_in)
        self.set_dimensions(dimensions)
        self.set_type_arguments(type_arguments)

    def set_type_arguments(self, type_arguments):
        # First, remove all tokens from the previous value of type_arguments
        for x in self._type_arguments_tokens:
            self.tokens.remove(x)
        # Collect any new tokens if required
        if type_arguments is AnonymousSE:
            self._type_arguments_tokens = type_arguments.tokens
            self.tokens.extend(self._type_arguments_tokens)
            type_arguments = type_arguments.value
        if type_arguments == 'diamond':
            # "Diamond" is an acceptable value for type arguments. I.E "<>"
            self._type_arguments = type_arguments
        else:
            # Ensure Type on all of the elements in the list, if it is one.
            if isinstance(type_arguments, list):
                for i in range(len(type_arguments)):
                    if isinstance(type_arguments[i], str):
                        type_arguments[i] = Type.ensure(type_arguments[i])

            from plyj.model.classes import Wildcard
            self._type_arguments = self._assert_list(type_arguments,
                                                     (Type, Wildcard))

    def set_enclosed_in(self, enclosed_in):
        self._enclosed_in = assert_none_or_ensure(enclosed_in, Type)

    def set_dimensions(self, dimensions):
        self._dimensions = AnonymousSE.ensure(dimensions)

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
    name = property(attrgetter("_name"))
    extends = property(attrgetter("_extends"))

    def __init__(self, name, extends=None):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends']

        self._name = Name.ensure(name, True)
        self._extends = self._assert_list_ensure(extends, Type)