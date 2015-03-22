#!/usr/bin/env python2
from operator import attrgetter
from types import NoneType
from plyj.model.expression import ArrayInitializer
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Expression
from plyj.utility import assert_none_or, assert_type, serialize_dimensions


class Variable(SourceElement):
    # I would like to remove this class. In theory, the dimension could be
    # added to the type but this means variable declarations have to be changed
    # somehow. Consider 'int i, j[];'. In this case there currently is only one
    # type with two variable declarators; This closely resembles the source
    # code. If the variable is to go away, the type has to be duplicated for
    # every variable...
    name = property(attrgetter("_name"))
    dimensions = property(attrgetter("_dimensions"))

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']

        self._name = None
        self._dimensions = None

        self.name = name
        self.dimensions = dimensions

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @dimensions.setter
    def dimensions(self, dimensions):
        dimensions = self._alter_tokens("dimensions", dimensions)
        self._dimensions = assert_type(dimensions, int)

    def serialize(self):
        return self.name.serialize() + serialize_dimensions(self.dimensions)


class VariableDeclarator(SourceElement):
    variable = property(attrgetter("_variable"))
    initializer = property(attrgetter("_initializer"))

    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']

        self._variable = None
        self._initializer = None

        self.variable = variable
        self.initializer = initializer

    @variable.setter
    def variable(self, variable):
        self._variable = assert_type(variable, Variable)

    @initializer.setter
    def initializer(self, initializer):
        self._initializer = assert_none_or(initializer,
                                           (Expression, ArrayInitializer))

    def serialize(self):
        if self.initializer is None:
            return self.variable.serialize()
        else:
            return (self.variable.serialize() + " = " +
                    self.initializer.serialize())