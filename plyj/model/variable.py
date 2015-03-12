#!/usr/bin/env python2
from plyj.model.expression import ArrayInitializer
from plyj.model.name import Name, ensure_name
from plyj.model.source_element import SourceElement, ensure_se, \
    AnonymousSourceElement, Expression


class Variable(SourceElement):
    # I would like to remove this class. In theory, the dimension could be
    # added to the type but this means variable declarations have to be changed
    # somehow. Consider 'int i, j[];'. In this case there currently is only one
    # type with two variable declarators; This closely resembles the source
    # code. If the variable is to go away, the type has to be duplicated for
    # every variable...

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']

        dimensions = ensure_se(dimensions)

        name = ensure_name(name, True)
        assert isinstance(dimensions, AnonymousSourceElement)

        self.name = name
        self.dimensions = dimensions


class VariableDeclarator(SourceElement):
    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']

        assert isinstance(variable, Variable)
        assert (initializer is None
                or isinstance(initializer, (AnonymousSourceElement,
                                            Expression, ArrayInitializer)))

        self.variable = variable
        self.initializer = initializer