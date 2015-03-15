#!/usr/bin/env python2
from operator import attrgetter
from types import NoneType
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Expression, \
    Declaration
from plyj.model.type import Type
from plyj.utility import assert_type, assert_none_or


class BinaryExpression(Expression):
    operator = property(attrgetter("_operator"))
    lhs = property(attrgetter("_lhs"))
    rhs = property(attrgetter("_rhs"))

    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs']

        self._operator = AnonymousSE.ensure(operator)
        self._lhs = assert_type(lhs, Expression)
        if self._operator.value == "instanceof":
            self._rhs = Type.ensure(rhs)
        else:
            self._rhs = assert_type(rhs, Expression)


class Assignment(BinaryExpression):
    pass


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


class Conditional(Expression):
    predicate = property(attrgetter("_predicate"))
    if_true = property(attrgetter("_if_true"))
    if_false = property(attrgetter("_if_false"))

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']

        self._predicate = assert_type(predicate, Expression)
        self._if_true = assert_type(if_true, Expression)
        self._if_false = assert_type(if_false, Expression)


class Unary(Expression):
    sign = property(attrgetter("_sign"))
    expression = property(attrgetter("_expression"))

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression']

        self._sign = AnonymousSE.ensure(sign)
        self._expression = assert_type(expression, Expression)


class Cast(Expression):
    target = property(attrgetter("_target"))
    expression = property(attrgetter("_expression"))

    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression']

        self._target = Type.ensure(target)
        self._expression = assert_type(expression, Expression)


def assert_target(target):
    if target is None:
        return None
    elif isinstance(target, Expression):
        return target
    else:
        return Name.ensure(target, False)


class MethodInvocation(Expression):
    name = property(attrgetter("_name"))
    arguments = property(attrgetter("_arguments"))
    type_arguments = property(attrgetter("_type_arguments"))
    target = property(attrgetter("_target"))

    def __init__(self, name, arguments=None, type_arguments=None, target=None):
        super(MethodInvocation, self).__init__()
        self._fields = ['name', 'arguments', 'type_arguments', 'target']

        self._name = Name.ensure(name, True)
        self._arguments = self._assert_list(arguments, Expression)
        self._type_arguments = self._assert_list_ensure(type_arguments, Type)
        self._target = assert_target(target)


class InstanceCreation(Expression):
    instance_type = property(attrgetter("_instance_type"))
    type_arguments = property(attrgetter("_type_arguments"))
    arguments = property(attrgetter("_arguments"))
    body = property(attrgetter("_body"))
    enclosed_in = property(attrgetter("_enclosed_in"))

    def __init__(self, instance_type, type_arguments=None, arguments=None,
                 body=None, enclosed_in=None):
        super(InstanceCreation, self).__init__()
        self._fields = ['type', 'type_arguments', 'arguments', 'body',
                        'enclosed_in']

        self._instance_type = Type.ensure(instance_type)
        self._type_arguments = self._assert_list_ensure(type_arguments, Type)
        self._arguments = self._assert_list(arguments, Expression)
        self._body = self._assert_list(body, Declaration)
        self._enclosed_in = assert_none_or(enclosed_in, Expression)


class FieldAccess(Expression):
    name = property(attrgetter("_name"))
    target = property(attrgetter("_target"))

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target']

        self._name = Name.ensure(name, True)
        self._target = assert_target(target)


class ArrayAccess(Expression):
    index = property(attrgetter("_index"))
    target = property(attrgetter("_target"))

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']

        self._name = assert_type(index, Expression)
        self._target = assert_target(target)


class ArrayCreation(Expression):
    type = property(attrgetter("_type"))
    dimensions = property(attrgetter("_dimensions"))
    initializer = property(attrgetter("_initializer"))

    def __init__(self, type_, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']

        if isinstance(dimensions, list):
            for i, d in enumerate(dimensions):
                dimensions[i] = self._absorb_ase_tokens(d)

        self._type = Type.ensure(type_)
        self._dimensions = None
        self._initializer = assert_none_or(initializer, ArrayInitializer)

        self.set_dimensions(dimensions)

    def set_dimensions(self, dimensions):
        self._dimensions = self._assert_list(dimensions,
                                             (NoneType, Expression))


class ArrayInitializer(SourceElement):
    elements = property(attrgetter("_elements"))

    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']

        # Multi-dimensional arrays force the ArrayInitalizer to also be
        # accepted
        from plyj.model.annotation import Annotation
        self._elements = self._assert_list(elements, (ArrayInitializer,
                                                      Expression,
                                                      Annotation))