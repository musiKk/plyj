#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE
from plyj.utility import assert_none_or_ensure, serialize_type_arguments, \
    serialize_dimensions


class Type(SourceElement):
    name = property(attrgetter("_name"))
    type_arguments = property(attrgetter("_type_arguments"))
    enclosed_in = property(attrgetter("_enclosed_in"))
    dimensions = property(attrgetter("_dimensions"))

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']

        self._name = None
        self._type_arguments = None
        self._dimensions = None
        self._enclosed_in = None

        self.name = name
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions
        self.type_arguments = type_arguments

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, False)

    @type_arguments.setter
    def type_arguments(self, type_arguments):
        # Replace tokens
        type_arguments = self._alter_tokens("type_arguments", type_arguments)

        if isinstance(type_arguments, str) and type_arguments == 'diamond':
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

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = AnonymousSE.ensure(dimensions)

    @enclosed_in.setter
    def enclosed_in(self, enclosed_in):
        self._enclosed_in = assert_none_or_ensure(enclosed_in, Type)

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
        assert isinstance(type_, str)
        return type_ in ["boolean", "void", "byte", "short", "int", "long",
                         "char", "float", "double"]

    def serialize(self):
        enclosed_in = ""
        if self.enclosed_in is not None:
            enclosed_in += self.enclosed_in.serialize() + "."
        type_args = serialize_type_arguments(self.type_arguments)
        dimensions = serialize_dimensions(self.dimensions)
        return enclosed_in + self.name.serialize() + type_args + dimensions


class TypeParameter(SourceElement):
    """
    Represents a type parameter in the definition of a class.
    """
    name = property(attrgetter("_name"))
    extends = property(attrgetter("_extends"))

    def __init__(self, name, extends=None):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends']

        self._name = None
        self._extends = None

        self.name = name
        self.extends = extends

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @extends.setter
    def extends(self, extends):
        self._extends = self._assert_list_ensure(extends, Type)

    def serialize(self):
        extends = ""
        if len(self.extends) != 0:
            extends = " & ".join([x.serialize() for x in self.extends])
            extends = " extends " + extends
        return self.name.serialize() + extends