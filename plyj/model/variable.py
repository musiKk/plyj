#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


class Variable(SourceElement):
    # I would like to remove this class. In theory, the dimension could be
    # added to the type but this means variable declarations have to be changed
    # somehow. Consider 'int i, j[];'. In this case there currently is only one
    # type with two variable declarators; This closely resembles the source
    # code. If the variable is to go away, the type has to be duplicated for
    # every variable...

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__(None)
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions


class VariableDeclarator(SourceElement):
    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__(None)
        self._fields = ['variable', 'initializer']
        self.variable = variable
        self.initializer = initializer