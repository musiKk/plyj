#!/usr/bin/env python2
from plyj.model.source_element import SourceElement
from plyj.model.classes import FieldDeclaration


class Statement(SourceElement):
    pass


class Empty(Statement):
    pass


class Block(Statement):
    def __init__(self, statements=None):
        super(Statement, self).__init__(None)
        self._fields = ['statements']
        if statements is None:
            statements = []
        self.statements = statements

    def __iter__(self):
        for s in self.statements:
            yield s


class VariableDeclaration(Statement, FieldDeclaration):
    pass


class ArrayInitializer(SourceElement):
    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__(None)
        self._fields = ['elements']
        if elements is None:
            elements = []
        self.elements = elements


class IfThenElse(Statement):
    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__(None)
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false


class While(Statement):
    def __init__(self, predicate, body=None):
        super(While, self).__init__(None)
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body


class For(Statement):
    def __init__(self, init, predicate, update, body):
        super(For, self).__init__(None)
        self._fields = ['init', 'predicate', 'update', 'body']
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body


class ForEach(Statement):
    def __init__(self, foreach_type, variable, iterable, body, modifiers=None):
        super(ForEach, self).__init__(None)
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = foreach_type
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers


class Assert(Statement):
    def __init__(self, predicate, message=None):
        super(Assert, self).__init__(None)
        self._fields = ['predicate', 'message']
        self.predicate = predicate
        self.message = message


class Switch(Statement):
    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__(None)
        self._fields = ['expression', 'switch_cases']
        self.expression = expression
        self.switch_cases = switch_cases


class SwitchCase(SourceElement):
    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__(None)
        self._fields = ['cases', 'body']
        if body is None:
            body = []
        self.cases = cases
        self.body = body


class DoWhile(Statement):
    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__(None)
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body


class Continue(Statement):
    def __init__(self, label=None):
        super(Continue, self).__init__(None)
        self._fields = ['label']
        self.label = label


class Break(Statement):
    def __init__(self, label=None):
        super(Break, self).__init__(None)
        self._fields = ['label']
        self.label = label


class Return(Statement):
    def __init__(self, result=None):
        super(Return, self).__init__(None)
        self._fields = ['result']
        self.result = result


class Synchronized(Statement):
    def __init__(self, monitor, body):
        super(Synchronized, self).__init__(None)
        self._fields = ['monitor', 'body']
        self.monitor = monitor
        self.body = body


class Throw(Statement):
    def __init__(self, exception):
        super(Throw, self).__init__(None)
        self._fields = ['exception']
        self.exception = exception


class Try(Statement):
    def __init__(self, block, catches=None, _finally=None, resources=None):
        super(Try, self).__init__(None)
        self._fields = ['block', 'catches', '_finally', 'resources']
        if catches is None:
            catches = []
        if resources is None:
            resources = []
        self.block = block
        self.catches = catches
        self._finally = _finally
        self.resources = resources

    def accept(self, visitor):
        if visitor.visit_Try(self):
            for s in self.block:
                s.accept(visitor)
        for c in self.catches:
            visitor.visit_Catch(c)
        if self._finally:
            self._finally.accept(visitor)


class Catch(SourceElement):
    def __init__(self, variable, modifiers=None, types=None, block=None):
        super(Catch, self).__init__(None)
        self._fields = ['variable', 'modifiers', 'types', 'block']
        if modifiers is None:
            modifiers = []
        if types is None:
            types = []
        self.variable = variable
        self.modifiers = modifiers
        self.types = types
        self.block = block


class Resource(SourceElement):
    """
    Part of Java's try-with-resources statement:
    http://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html
    In:

        try (X x = new X()) {

        }

    where X implements java.lang.AutoCloseable, then "x" is a resource.
    """
    def __init__(self, variable, resource_type=None,
                 modifiers=None, initializer=None):
        super(Resource, self).__init__(None)
        self._fields = ['variable', 'type', 'modifiers', 'initializer']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = resource_type
        self.modifiers = modifiers
        self.initializer = initializer


class ConstructorInvocation(Statement):
    """
    An explicit invocations of a class's constructor.

    This is a variant of either this() or super(), NOT a "new" expression.
    """

    def __init__(self, name, target=None, type_arguments=None, arguments=None):
        super(ConstructorInvocation, self).__init__(None)
        self._fields = ['name', 'target', 'type_arguments', 'arguments']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments


class ExpressionStatement(Statement):
    def __init__(self, expression):
        super(ExpressionStatement, self).__init__(None)
        self._fields = ['expression']
        self.expression = expression