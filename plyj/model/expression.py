#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


class Expression(SourceElement):
    def __init__(self):
        super(Expression, self).__init__(None)
        self._fields = []


class BinaryExpression(Expression):
    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs


class Assignment(BinaryExpression):
    pass


class Conditional(Expression):
    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false


class ConditionalOr(BinaryExpression):
    pass


class ConditionalAnd(BinaryExpression):
    pass


class Or(BinaryExpression):
    pass


class Xor(BinaryExpression):
    pass


class And(BinaryExpression):
    pass


class Equality(BinaryExpression):
    pass


class InstanceOf(BinaryExpression):
    pass


class Relational(BinaryExpression):
    pass


class Shift(BinaryExpression):
    pass


class Additive(BinaryExpression):
    pass


class Multiplicative(BinaryExpression):
    pass


class Unary(Expression):
    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression']
        self.sign = sign
        self.expression = expression


class Cast(Expression):
    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression']
        self.target = target
        self.expression = expression


class MethodInvocation(Expression):
    def __init__(self, name, arguments=None, type_arguments=None, target=None):
        super(MethodInvocation, self).__init__()
        self._fields = ['name', 'arguments', 'type_arguments', 'target']
        if arguments is None:
            arguments = []
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.arguments = arguments
        self.type_arguments = type_arguments
        self.target = target


class InstanceCreation(Expression):

    def __init__(self, instance_type, type_arguments=None, arguments=None,
                 body=None, enclosed_in=None):
        super(InstanceCreation, self).__init__()
        self._fields = [
            'type', 'type_arguments', 'arguments', 'body', 'enclosed_in']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = instance_type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in


class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target']
        self.name = name
        self.target = target


class ArrayAccess(Expression):

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']
        self.index = index
        self.target = target


class ArrayCreation(Expression):

    def __init__(self, array_type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']
        if dimensions is None:
            dimensions = []
        self.type = array_type
        self.dimensions = dimensions
        self.initializer = initializer