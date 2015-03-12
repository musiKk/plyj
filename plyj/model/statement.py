#!/usr/bin/env python2
from plyj.model.literal import Literal
from plyj.model.name import Name, ensure_name
from plyj.model.source_element import SourceElement, ensure_se, \
    AnonymousSourceElement, Statement, Expression
from plyj.model.classes import FieldDeclaration
from plyj.model.type import Type, TypeParameter


def _assert_ensure_ase(modifiers):
    for i in range(len(modifiers)):
        modifiers[i] = ensure_se(modifiers[i])
        assert isinstance(modifiers[i], AnonymousSourceElement)


class Empty(Statement):
    pass


class Block(Statement):
    def __init__(self, statements=None):
        super(Statement, self).__init__()
        self._fields = ['statements']
        if statements is None:
            statements = []

        assert isinstance(statements, list)
        for x in statements:
            assert isinstance(x, Statement)

        self.statements = statements

    def __iter__(self):
        for s in self.statements:
            yield s


class VariableDeclaration(Statement, FieldDeclaration):
    pass


class IfThenElse(Statement):
    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']

        assert isinstance(predicate, Expression)
        assert isinstance(if_true, Statement)
        assert if_false is None or isinstance(if_false, Statement)

        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false


class While(Statement):
    def __init__(self, predicate, body=None):
        super(While, self).__init__()
        self._fields = ['predicate', 'body']

        assert isinstance(predicate, Expression)
        assert isinstance(body, Statement)

        self.predicate = predicate
        self.body = body


class For(Statement):
    def __init__(self, init, predicate, update, body):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body']

        assert isinstance(init, Expression)
        assert isinstance(update, Expression)
        assert isinstance(predicate, Expression)
        assert isinstance(body, Statement)

        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body


class ForEach(Statement):
    def __init__(self, foreach_type, variable, iterable, body, modifiers=None):
        super(ForEach, self).__init__()
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers']

        if modifiers is None:
            modifiers = []

        foreach_type = ensure_se(foreach_type)

        assert isinstance(foreach_type, (Type, AnonymousSourceElement))
        assert isinstance(variable, VariableDeclaration)
        assert isinstance(iterable, Expression)
        assert isinstance(body, Statement)
        assert isinstance(modifiers, list)
        _assert_ensure_ase(modifiers)

        self.type = foreach_type
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers


class Assert(Statement):
    def __init__(self, predicate, message=None):
        super(Assert, self).__init__()
        self._fields = ['predicate', 'message']

        assert isinstance(predicate, Expression)
        assert isinstance(message, Literal)

        self.predicate = predicate
        self.message = message


class Switch(Statement):
    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases']

        assert isinstance(expression, Expression)
        assert isinstance(switch_cases, [])

        self.expression = expression
        self.switch_cases = switch_cases


class SwitchCase(SourceElement):
    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body']
        if body is None:
            body = []

        assert isinstance(cases, list)
        assert isinstance(body, list)
        _assert_ensure_ase(cases)
        for x in body:
            assert isinstance(x, Statement)

        self.cases = cases
        self.body = body


class DoWhile(Statement):
    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body']

        assert isinstance(predicate, Expression)
        assert body is None or isinstance(body, Statement)

        self.predicate = predicate
        self.body = body


class Continue(Statement):
    def __init__(self, label=None):
        super(Continue, self).__init__()
        self._fields = ['label']

        if label is not None:
            label = ensure_name(label, True)

        self.label = label


class Break(Statement):
    def __init__(self, label=None):
        super(Break, self).__init__()
        self._fields = ['label']

        if label is not None:
            label = ensure_name(label, True)

        self.label = label


class Return(Statement):
    def __init__(self, result=None):
        super(Return, self).__init__()
        self._fields = ['result']

        assert result is None or isinstance(result, Expression)

        self.result = result


class Synchronized(Statement):
    def __init__(self, monitor, body):
        super(Synchronized, self).__init__()
        self._fields = ['monitor', 'body']

        assert isinstance(monitor, Expression)
        assert isinstance(body, Statement)

        self.monitor = monitor
        self.body = body


class Throw(Statement):
    def __init__(self, exception):
        super(Throw, self).__init__()
        self._fields = ['exception']

        assert exception is None or isinstance(exception, Expression)

        self.exception = exception


class Try(Statement):
    def __init__(self, block, catches=None, _finally=None, resources=None):
        super(Try, self).__init__()
        self._fields = ['block', 'catches', '_finally', 'resources']
        if catches is None:
            catches = []
        if resources is None:
            resources = []

        assert isinstance(catches, list)
        assert isinstance(resources, list)
        assert isinstance(_finally, Block)
        assert isinstance(block, Block)

        for x in catches:
            assert isinstance(x, Catch)
        for x in resources:
            assert isinstance(x, Resource)

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
        super(Catch, self).__init__()
        self._fields = ['variable', 'modifiers', 'types', 'block']
        if modifiers is None:
            modifiers = []
        if types is None:
            types = []

        assert isinstance(variable, VariableDeclaration)
        assert isinstance(modifiers, list)
        assert isinstance(types, list)
        assert isinstance(block, Block)

        _assert_ensure_ase(modifiers)
        for x in types:
            assert isinstance(x, Type)

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
        super(Resource, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'initializer']
        if modifiers is None:
            modifiers = []

        assert isinstance(variable, VariableDeclaration)
        assert isinstance(modifiers, list)
        assert isinstance(resource_type, Type)
        assert isinstance(initializer, Expression)

        _assert_ensure_ase(modifiers)

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
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'type_arguments', 'arguments']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []

        name = ensure_name(name, True)
        if target is not None:
            target = ensure_name(target, True)
        assert isinstance(type_arguments, list)
        assert isinstance(arguments, list)

        for x in type_arguments:
            assert isinstance(x, TypeParameter)
        for x in arguments:
            assert isinstance(x, VariableDeclaration)

        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments


class ExpressionStatement(Statement):
    def __init__(self, expression):
        super(ExpressionStatement, self).__init__()
        self._fields = ['expression']
        assert isinstance(expression, Expression)
        self.expression = expression