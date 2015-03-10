#!/usr/bin/env python2
from plyj.model.source_element import SourceElement
from plyj.model.type import Type


class Literal(SourceElement):

    def __init__(self, value):
        super(Literal, self).__init__()
        self._fields = ['value']

        assert isinstance(value, (int, bool, float, str))
        self.value = value


class ClassLiteral(SourceElement):

    def __init__(self, class_type):
        super(ClassLiteral, self).__init__()
        self._fields = ['type']
        assert isinstance(class_type, Type)
        self.type = class_type