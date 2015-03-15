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

        self._value = assert_type(value, (int, bool, float, str))


class ClassLiteral(Expression):
    type = property(attrgetter("_type"))

    def __init__(self, type_):
        super(ClassLiteral, self).__init__()
        self._fields = ['type']

        self._type = Type.ensure(type_)