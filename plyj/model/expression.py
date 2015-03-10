#!/usr/bin/env python2
from plyj.model.literal import Literal
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, ensure_se, \
    AnonymousSourceElement, Expression, Statement
from plyj.model.statement import VariableDeclaration
from plyj.model.type import Type, TypeParameter


class BinaryExpression(Expression):
    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs']

        operator = ensure_se(operator)
        assert isinstance(lhs, SourceElement)
        assert isinstance(rhs, SourceElement)

        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs


class Assignment(BinaryExpression):
    pass


class Conditional(Expression):
    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        assert isinstance(predicate, SourceElement)
        assert isinstance(if_true, SourceElement)
        assert isinstance(if_false, SourceElement)
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
        sign = ensure_se(sign)
        assert isinstance(expression, (Expression, Name))
        self.sign = sign
        self.expression = expression


class Cast(Expression):
    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression']
        target = ensure_se(target)
        assert isinstance(expression, (Expression, Name))
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

        name = ensure_se(name)
        target = ensure_se(target)
        assert isinstance(name, (Name, AnonymousSourceElement))
        assert isinstance(arguments, list)
        assert isinstance(type_arguments, list)

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

        instance_type = ensure_se(instance_type)
        enclosed_in = ensure_se(enclosed_in)

        assert isinstance(instance_type, (Type, AnonymousSourceElement))
        assert isinstance(arguments, list)
        assert isinstance(type_arguments, list)
        assert isinstance(body, list)
        assert isinstance(enclosed_in, (Name, AnonymousSourceElement))

        for x in arguments:
            assert isinstance(x, VariableDeclaration)
        for x in type_arguments:
            assert isinstance(x, TypeParameter)
        for x in body:
            assert isinstance(x, Statement)

        self.type = instance_type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in


class FieldAccess(Expression):
    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        name = ensure_se(name)
        target = ensure_se(target)

        assert isinstance(name, (Name, AnonymousSourceElement))
        assert isinstance(target, (Name, AnonymousSourceElement))

        self._fields = ['name', 'target']
        self.name = name
        self.target = target


class ArrayAccess(Expression):
    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']

        index = ensure_se(index)
        target = ensure_se(target)
        assert isinstance(target, (Name, AnonymousSourceElement))

        self.index = index
        self.target = target


class ArrayCreation(Expression):
    def __init__(self, array_type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']

        if dimensions is None:
            dimensions = []

        array_type = ensure_se(array_type)

        assert isinstance(array_type, (Type, AnonymousSourceElement))
        assert isinstance(dimensions, list)
        assert isinstance(initializer, ArrayInitializer)

        for i in range(len(dimensions)):
            dimensions[i] = ensure_se(dimensions[i])

        self.type = array_type
        self.dimensions = dimensions
        self.initializer = initializer


class ArrayInitializer(SourceElement):
    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']
        if elements is None:
            elements = []

        assert isinstance(elements, list)

        for e in elements:
            assert isinstance(e, (Literal, Expression, AnonymousSourceElement))

        self.elements = elements