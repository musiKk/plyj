#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


class Literal(SourceElement):

    def __init__(self, value):
        super(Literal, self).__init__(None)
        self._fields = ['value']
        self.value = value


class ClassLiteral(SourceElement):

    def __init__(self, class_type):
        super(ClassLiteral, self).__init__(None)
        self._fields = ['type']
        self.type = class_type


class Name(SourceElement):

    def __init__(self, value):
        super(Name, self).__init__(None)
        self._fields = ['value']
        self.value = value

    def append_name(self, name):
        if hasattr(name, "value") and isinstance(name.value, str):
            self.value = self.value + '.' + name.value
        else:
            self.value = self.value + '.' + name