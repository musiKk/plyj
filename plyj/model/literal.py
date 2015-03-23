#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.source_element import Expression
from plyj.model.type import Type
from plyj.utility import assert_type


class Literal(Expression):
    value = property(attrgetter("_value"))

    def __init__(self, value):
        super(Literal, self).__init__()
        self._fields = ['value']

        self._value = None

        self.value = value

    @value.setter
    def value(self, value):
        self._value = assert_type(value, (int, bool, float, str))

    def serialize(self):
        if isinstance(self.value, bool):
            return "true" if self.value else "false"
        if isinstance(self.value, (int, float)):
            return self.value
        # No need to escape string because it is already escaped.
        # Value already has quotes too.
        return self.value


class ClassLiteral(Expression):
    type = property(attrgetter("_type"))

    def serialize(self):
        return self.type.serialize() + ".class"

    def __init__(self, type_):
        super(ClassLiteral, self).__init__()
        self._fields = ['type']

        self._type = None

        self.type = type_

    @type.setter
    def type(self, type_):
        self._type = Type.ensure(type_)