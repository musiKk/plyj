#!/usr/bin/env python2
from operator import attrgetter
from types import NoneType
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, AnonymousSE, Expression, \
    Declaration
from plyj.model.type import Type
from plyj.utility import assert_type, assert_none_or, serialize_arguments, \
    serialize_type_arguments, serialize_dimensions, serialize_body


# When serializing a Unary Expression, it is very important that the Unary
# operator does not get combined with another immediately successive unary
# operator. Therefore, we will check the symbol directly after the Unary and
# insert a space if there could be any confusion
UNARY_SPACE_TRIGGERS = "-+~!"


class BinaryExpression(Expression):
    operator = property(attrgetter("_operator"))
    lhs = property(attrgetter("_lhs"))
    rhs = property(attrgetter("_rhs"))

    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs']

        self._operator = None
        self._lhs = None
        self._rhs = None

        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    @operator.setter
    def operator(self, operator):
        self._operator = AnonymousSE.ensure(operator)

    @lhs.setter
    def lhs(self, lhs):
        self._lhs = assert_type(lhs, Expression)

    @rhs.setter
    def rhs(self, rhs):
        if self._operator.value == "instanceof":
            self._rhs = Type.ensure(rhs)
        else:
            self._rhs = assert_type(rhs, Expression)

    def serialize(self):
        """
        Some of the files in the oracle JDK deal with HUGE binary expression
        trees. So I had to convert this function to an iterative solution
        rather than the far more natural recursive one.
        :return:
        """
        stack = []
        current = self
        retn = ""
        while True:
            if not isinstance(current, BinaryExpression):
                retn += current.serialize()
                while current is stack[-1].rhs:
                    current = stack.pop()
                    if len(stack) == 0:
                        return retn
                retn += " "
                retn += stack[-1].operator.serialize()
                retn += " "
                current = stack[-1].rhs
            else:
                stack.append(current)
                current = current.lhs
        return retn


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


class BracketedExpression(Expression):
    value = property(attrgetter("_value"))

    def __init__(self, value):
        super(self.__class__, self).__init__()
        self._fields = ['value']

        self._value = None
        self.value = value

    @value.setter
    def value(self, value):
        self._value = assert_type(value, Expression)

    def serialize(self):
        return "({})".format(
            self.value.serialize(),
        )


class Conditional(Expression):
    predicate = property(attrgetter("_predicate"))
    if_true = property(attrgetter("_if_true"))
    if_false = property(attrgetter("_if_false"))

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']

        self._predicate = None
        self._if_true = None
        self._if_false = None

        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false

    @predicate.setter
    def predicate(self, predicate):
        self._predicate = assert_type(predicate, Expression)

    @if_true.setter
    def if_true(self, if_true):
        self._if_true = assert_type(if_true, Expression)

    @if_false.setter
    def if_false(self, if_false):
        self._if_false = assert_type(if_false, Expression)

    def serialize(self):
        return "{} ? {} : {}".format(
            self.predicate.serialize(),
            self.if_true.serialize(),
            self.if_false.serialize()
        )


class Unary(Expression):
    sign = property(attrgetter("_sign"))
    expression = property(attrgetter("_expression"))

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression']

        self._sign = None
        self._expression = None

        self.sign = sign
        self.expression = expression

    @sign.setter
    def sign(self, sign):
        self._sign = AnonymousSE.ensure(sign)

    @expression.setter
    def expression(self, expression):
        self._expression = assert_type(expression, Expression)

    def serialize(self):
        sign = self.sign.serialize()
        expression = self.expression.serialize()
        if expression[0] in UNARY_SPACE_TRIGGERS:
            expression = " " + expression
        if sign == "x++":
            return expression + "++"
        elif sign == "x--":
            return expression + "--"
        elif sign == "++x":
            return "++" + expression
        elif sign == "--x":
            return "--" + expression
        else:
            return sign + expression


class Cast(Expression):
    target = property(attrgetter("_target"))
    expression = property(attrgetter("_expression"))

    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression']

        self._target = None
        self._expression = None

        self.target = target
        self.expression = expression

    @expression.setter
    def expression(self, expression):
        self._expression = assert_type(expression, Expression)

    @target.setter
    def target(self, target):
        self._target = Type.ensure(target)

    def serialize(self):
        return "({}){}".format(
            self.target.serialize(),
            self.expression.serialize(),
        )


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

        self._name = None
        self._arguments = None
        self._type_arguments = None
        self._target = None

        self.name = name
        self.arguments = arguments
        self.type_arguments = type_arguments
        self.target = target

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @arguments.setter
    def arguments(self, arguments):
        self._arguments = self._assert_list(arguments, Expression)

    @type_arguments.setter
    def type_arguments(self, type_arguments):
        self._type_arguments = self._assert_list_ensure(type_arguments, Type)

    @target.setter
    def target(self, target):
        self._target = assert_target(target)

    def serialize(self):
        if self.target is None:
            target = ""
        else:
            target = self.target.serialize() + "."
        return "{}{}{}{}".format(
            target,
            serialize_type_arguments(self.type_arguments),
            self.name.serialize(),
            serialize_arguments(self.arguments)
        )


class InstanceCreation(Expression):
    type = property(attrgetter("_type"))
    type_arguments = property(attrgetter("_type_arguments"))
    arguments = property(attrgetter("_arguments"))
    body = property(attrgetter("_body"))
    enclosed_in = property(attrgetter("_enclosed_in"))

    def __init__(self, type_, type_arguments=None, arguments=None,
                 body=None, enclosed_in=None):
        super(InstanceCreation, self).__init__()
        self._fields = ['type', 'type_arguments', 'arguments', 'body',
                        'enclosed_in']

        self._type = None
        self._type_arguments = None
        self._arguments = None
        self._body = None
        self._enclosed_in = None

        self.type = type_
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in

    @type.setter
    def type(self, type_):
        self._type = Type.ensure(type_)

    @type_arguments.setter
    def type_arguments(self, type_arguments):
        self._type_arguments = self._assert_list_ensure(type_arguments, Type)

    @arguments.setter
    def arguments(self, arguments):
        self._arguments = self._assert_list(arguments, Expression)

    @body.setter
    def body(self, body):
        self._body = self._assert_list(body, Declaration)

    @enclosed_in.setter
    def enclosed_in(self, enclosed_in):
        self._enclosed_in = assert_none_or(enclosed_in, Expression)

    def serialize(self):
        if self.enclosed_in is None:
            target = ""
        else:
            target = self.enclosed_in.serialize() + "."
        return "{}new {}{}{}{}".format(
            target,
            serialize_type_arguments(self.type_arguments),
            self.type.serialize(),
            serialize_arguments(self.arguments),
            " " + serialize_body(self.body, "") if len(self.body) > 0 else ""
        )


class FieldAccess(Expression):
    name = property(attrgetter("_name"))
    target = property(attrgetter("_target"))

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target']

        self._name = None
        self._target = None

        self.name = name
        self.target = target

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @target.setter
    def target(self, target):
        self._target = assert_target(target)

    def serialize(self):
        if self.target is None:
            target = ""
        else:
            target = self.target.serialize() + "."
        return target + self.name.serialize()


class ArrayAccess(Expression):
    index = property(attrgetter("_index"))
    target = property(attrgetter("_target"))

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']

        self._index = None
        self._target = None

        self.index = index
        self.target = target

    @index.setter
    def index(self, index):
        self._index = assert_type(index, Expression)

    @target.setter
    def target(self, target):
        self._target = assert_target(target)
        assert self._target is not None

    def serialize(self):
        return self.target.serialize() + "[" + self.index.serialize() + "]"


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

        self._type = None
        self._dimensions = None
        self._initializer = None

        self.type = type_
        self.dimensions = dimensions
        self.initializer = initializer

    @type.setter
    def type(self, type_):
        self._type = Type.ensure(type_)

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = self._assert_list(dimensions,
                                             (NoneType, Expression))

    @initializer.setter
    def initializer(self, initializer):
        self._initializer = assert_none_or(initializer, ArrayInitializer)

    def serialize(self):
        if self.initializer is None:
            initializer = ""
        else:
            initializer = " " + self.initializer.serialize()
        return "new {}{}{}".format(
            self.type.serialize(),
            serialize_dimensions(self.dimensions),
            initializer
        )


class ArrayInitializer(SourceElement):
    elements = property(attrgetter("_elements"))

    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']

        self._elements = None

        self.elements = elements

    @elements.setter
    def elements(self, elements):
        # Multi-dimensional arrays force the ArrayInitalizer to also be
        # accepted
        from plyj.model.annotation import Annotation
        self._elements = self._assert_list(elements, (ArrayInitializer,
                                                      Expression,
                                                      Annotation))

    def serialize(self):
        return "{" + ", ".join([x.serialize() for x in self.elements]) + "}"