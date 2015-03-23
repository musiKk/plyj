#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, Statement, Expression, \
    Modifier, AnonymousSE, Declaration
from plyj.model.type import Type
from plyj.model.variable import VariableDeclarator, Variable
from plyj.utility import assert_type, assert_none_or, assert_none_or_ensure, \
    serialize_modifiers, serialize_body, serialize_type_arguments, \
    serialize_arguments, indent


def _format_block_or_statement(branch):
    if isinstance(branch, Block):
        return " " + branch.serialize()
    else:
        return "\n" + indent(branch.serialize())


class Empty(Statement):
    def statement_serialize(self):
        return ";"


class Block(Statement):
    statements = property(attrgetter("_statements"))

    def __init__(self, statements=None):
        super(Block, self).__init__()
        self._fields = ['statements']

        self._statements = None
        self.statements = statements

    def __iter__(self):
        for s in self.statements:
            yield s

    @statements.setter
    def statements(self, statements):
        self._statements = self._assert_body(statements)

    def statement_serialize(self):
        return serialize_body(self.statements)


class VariableDeclaration(Declaration, Statement):
    type = property(attrgetter("_type"))
    variable_declarators = property(attrgetter("_variable_declarators"))
    modifiers = property(attrgetter("_modifiers"))

    def __init__(self, type_, variable_declarators, modifiers=None):
        super(VariableDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']

        self._type = None
        self._variable_declarators = None
        self._modifiers = None

        self.type = type_
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers

    @type.setter
    def type(self, type_):
        self._type = Type.ensure(type_)

    @variable_declarators.setter
    def variable_declarators(self, variable_declarators):
        variable_declarators = self._alter_tokens("variable_decorators",
                                                  variable_declarators)
        self._variable_declarators = self._assert_list(variable_declarators,
                                                       VariableDeclarator)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    def _serialize(self):
        result = serialize_modifiers(self.modifiers)
        result += self.type.serialize()
        result += " "
        result += ", ".join([x.serialize() for x in self.variable_declarators])
        result += ";"
        return result

    def statement_serialize(self):
        return self._serialize()

    def serialize(self):
        return self._serialize()


class IfThenElse(Statement):
    predicate = property(attrgetter("_predicate"))
    if_true = property(attrgetter("_if_true"))
    if_false = property(attrgetter("_if_false"))

    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__()
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
        self._if_true = assert_none_or(if_true, Statement)

    @if_false.setter
    def if_false(self, if_false):
        self._if_false = assert_none_or(if_false, Statement)

    def statement_serialize(self):
        if_true = _format_block_or_statement(self.if_true)
        if self.if_false is None:
            return "if ({}) {}".format(self.predicate.serialize(), if_true)
        else:
            if_false = _format_block_or_statement(self.if_false)
            return "if ({}){}\nelse {}".format(self.predicate.serialize(),
                                               if_true, if_false)


class While(Statement):
    predicate = property(attrgetter("_predicate"))
    body = property(attrgetter("_body"))

    def __init__(self, predicate, body=None):
        super(While, self).__init__()
        self._fields = ['predicate', 'body']

        self._predicate = None
        self._body = None

        self.predicate = predicate
        self.body = body

    @predicate.setter
    def predicate(self, predicate):
        self._predicate = assert_type(predicate, Expression)

    @body.setter
    def body(self, body):
        self._body = assert_none_or(body, Statement)

    def statement_serialize(self):
        return "while ({}) {}".format(self.predicate.serialize(),
                                      _format_block_or_statement(self.body))


class For(Statement):
    init = property(attrgetter("_init"))
    predicate = property(attrgetter("_predicate"))
    update = property(attrgetter("_update"))
    body = property(attrgetter("_body"))

    def __init__(self, init, predicate, update, body):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body']

        if isinstance(init, VariableDeclaration):
            self._init = init
        else:
            self._init = self._assert_list(init, Expression)

        self._predicate = None
        self.predicate = predicate
        self._update = None
        self.update = update
        self._body = None
        self.body = body

    @predicate.setter
    def predicate(self, predicate):
        self._predicate = assert_none_or(predicate, Expression)

    @update.setter
    def update(self, update):
        self._update = self._assert_list(update, Expression)

    @body.setter
    def body(self, body):
        self._body = assert_type(body, Statement)

    def statement_serialize(self):
        if isinstance(self.init, VariableDeclaration):
            init = self.init.serialize()[:-1]
        else:
            init = ", ".join(x.serialize() for x in self.init)
        update = ", ".join([x.serialize() for x in self.update])
        predicate = ""
        if self.predicate is not None:
            predicate = self.predicate.serialize()
        body = ""
        if self.body is not None:
            body = _format_block_or_statement(self.body)
        return "for ({};{};{}) {}".format(init, predicate, update, body)


class ForEach(Statement):
    type = property(attrgetter("_type"))
    variable = property(attrgetter("_variable"))
    iterable = property(attrgetter("_iterable"))
    body = property(attrgetter("_body"))
    modifiers = property(attrgetter("_modifiers"))

    def __init__(self, type_, variable, iterable, body, modifiers=None):
        super(ForEach, self).__init__()
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers']

        self._type = None
        self._variable = None
        self._iterable = None
        self._body = None
        self._modifiers = None

        self.type = type_
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers

    @type.setter
    def type(self, type_):
        self._type = Type.ensure(type_)

    @variable.setter
    def variable(self, variable):
        self._variable = assert_type(variable, Variable)

    @iterable.setter
    def iterable(self, iterable):
        self._iterable = assert_type(iterable, Expression)

    @body.setter
    def body(self, body):
        self._body = assert_type(body, Statement)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    def statement_serialize(self):
        return "for ({}{} {} : {}) {}".format(
            serialize_modifiers(self.modifiers),
            self.type.serialize(),
            self.variable.serialize(),
            self.iterable.serialize(),
            _format_block_or_statement(self.body)
        )


class Assert(Statement):
    predicate = property(attrgetter("_predicate"))
    message = property(attrgetter("_message"))

    def __init__(self, predicate, message=None):
        super(Assert, self).__init__()
        self._fields = ['predicate', 'message']

        self._predicate = None
        self._message = None

        self.predicate = predicate
        self.message = message

    @predicate.setter
    def predicate(self, predicate):
        self._predicate = assert_type(predicate, Expression)

    @message.setter
    def message(self, message):
        self._message = assert_none_or(message, Expression)

    def statement_serialize(self):
        return "assert {}{};".format(
            self.predicate.serialize(),
            "" if self.message is None else " : " + self.message.serialize())


class Switch(Statement):
    expression = property(attrgetter("_expression"))
    switch_cases = property(attrgetter("_switch_cases"))

    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases']

        self._expression = None
        self._switch_cases = None

        self.expression = expression
        self.switch_cases = switch_cases

    @expression.setter
    def expression(self, expression):
        self._expression = assert_type(expression, Expression)

    @switch_cases.setter
    def switch_cases(self, switch_cases):
        self._switch_cases = self._assert_list(switch_cases, SwitchCase)

    def statement_serialize(self):
        return "switch ({}) {{\n{}\n}}\n".format(
            self.expression.serialize(),
            "".join([x.serialize() for x in self.switch_cases])
        )


class SwitchCase(SourceElement):
    cases = property(attrgetter("_cases"))
    body = property(attrgetter("_body"))
    default = property(attrgetter("_default"))

    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body']

        self._cases = None
        self._body = None
        self._default = False

        self.cases = cases
        self.body = body

    @cases.setter
    def cases(self, cases):
        default = False
        for i, c in enumerate(cases):
            if ((isinstance(c, Name) and c.value == "default") or
               (isinstance(c, AnonymousSE) and c.value == "default") or
               (isinstance(c, str) and c == "default")):
                default = True
                del cases[i]
                break

        self._default = default
        self._cases = self._assert_list(cases, Expression)

    @body.setter
    def body(self, body):
        self._body = self._assert_body(body)

    def serialize(self):
        result = ""
        for case in self.cases:
            result += "case " + case.serialize() + ":\n"
        if self.default:
            result += "default:\n"
        result += serialize_body(self.body, "", False)
        return result


class DoWhile(Statement):
    predicate = property(attrgetter("_predicate"))
    body = property(attrgetter("_body"))

    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body']

        self._predicate = None
        self._body = None

        self.predicate = predicate
        self.body = body

    @predicate.setter
    def predicate(self, predicate):
        self._predicate = assert_type(predicate, Expression)

    @body.setter
    def body(self, body):
        self._body = assert_none_or(body, Statement)

    def statement_serialize(self):
        return ("do" + _format_block_or_statement(self.body) + " while(" +
                self.predicate.serialize() + ");")


class Continue(Statement):
    label = property(attrgetter("_label"))

    def __init__(self, label=None):
        super(Continue, self).__init__()
        self._fields = ['label']

        self._label = None

        self.label = label

    @label.setter
    def label(self, label):
        self._label = assert_none_or_ensure(label, Name, True)

    def statement_serialize(self):
        if self.label is None:
            return "continue;"
        else:
            return "continue " + self.label.serialize() + ";"


class Break(Statement):
    label = property(attrgetter("_label"))

    def __init__(self, label=None):
        super(Break, self).__init__()
        self._fields = ['label']

        self._label = None

        self.label = label

    @label.setter
    def label(self, label):
        self._label = assert_none_or_ensure(label, Name, True)

    def statement_serialize(self):
        if self.label is None:
            return "break;"
        else:
            return "break " + self.label.serialize() + ";"


class Return(Statement):
    result = property(attrgetter("_result"))

    def __init__(self, result=None):
        super(Return, self).__init__()
        self._fields = ['result']

        self._result = None

        self.result = result

    @result.setter
    def result(self, result):
        self._result = assert_none_or(result, Expression)

    def statement_serialize(self):
        if self.result is None:
            return "return;"
        else:
            return "return " + self.result.serialize() + ";"


class Synchronized(Statement):
    monitor = property(attrgetter("_monitor"))
    body = property(attrgetter("_body"))

    def __init__(self, monitor, body):
        super(Synchronized, self).__init__()
        self._fields = ['monitor', 'body']

        self._monitor = None
        self._body = None

        self.monitor = monitor
        self.body = body

    @monitor.setter
    def monitor(self, monitor):
        self._monitor = assert_type(monitor, Expression)

    @body.setter
    def body(self, body):
        self._body = assert_type(body, Block)

    def statement_serialize(self):
        return ("synchronized (" + self.monitor.serialize() + ")" +
                _format_block_or_statement(self.body))


class Throw(Statement):
    exception = property(attrgetter("_exception"))

    def __init__(self, exception):
        super(Throw, self).__init__()
        self._fields = ['exception']

        self._exception = None

        self.exception = exception

    @exception.setter
    def exception(self, exception):
        self._exception = assert_type(exception, Expression)

    def statement_serialize(self):
        return "throw " + self.exception.serialize() + ";"


class Try(Statement):
    block = property(attrgetter("_block"))
    catches = property(attrgetter("_catches"))
    finally_ = property(attrgetter("_finally"))
    resources = property(attrgetter("_resources"))

    def __init__(self, block, catches=None, finally_=None, resources=None):
        super(Try, self).__init__()
        self._fields = ['block', 'catches', 'finally_', 'resources']

        self._block = None
        self._catches = None
        self._finally = None
        self._resources = None

        self.block = block
        self.catches = catches
        self.finally_ = finally_
        self.resources = resources

    @block.setter
    def block(self, block):
        self._block = assert_type(block, Block)

    @catches.setter
    def catches(self, catches):
        self._catches = self._assert_list(catches, Catch)

    @finally_.setter
    def finally_(self, finally_):
        self._finally = assert_none_or(finally_, Block)

    @resources.setter
    def resources(self, resources):
        self._resources = self._assert_list(resources, Resource)

    def accept(self, visitor):
        if visitor.visit_Try(self):
            for s in self.block:
                s.accept(visitor)
        for c in self.catches:
            visitor.visit_Catch(c)
        if self._finally:
            self._finally.accept(visitor)

    def statement_serialize(self):
        result = "try "
        if len(self.resources) > 0:
            resources = [x.serialize() for x in self.resources]
            result += "(" + "; ".join(resources) + ") "
        result += self.block.serialize()
        result += "\n".join([" " + x.serialize() for x in self.catches])
        if self.finally_ is not None:
            result += " finally " + self.finally_.serialize()
        return result


class Catch(SourceElement):
    variable = property(attrgetter("_variable"))
    modifiers = property(attrgetter("_modifiers"))
    types = property(attrgetter("_types"))
    block = property(attrgetter("_block"))

    def __init__(self, variable, modifiers=None, types=None, block=None):
        super(Catch, self).__init__()
        self._fields = ['variable', 'modifiers', 'types', 'block']

        self._variable = None
        self._modifiers = None
        self._types = None
        self._block = None

        self.variable = variable
        self.modifiers = modifiers
        self.types = types
        self.block = block

    @variable.setter
    def variable(self, variable):
        self._variable = assert_type(variable, Variable)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @types.setter
    def types(self, types):
        self._types = self._assert_list_ensure(types, Type)

    @block.setter
    def block(self, block):
        self._block = assert_none_or(block, Block)

    def serialize(self):
        result = "catch (" + serialize_modifiers(self.modifiers)
        result += " | ".join([x.serialize() for x in self.types])
        result += " " + self.variable.serialize()
        result += ") " + self.block.serialize()
        return result


class Resource(SourceElement):
    """
    Part of Java's try-with-resources statement:
    http://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html
    In:

        try (X x = new X()) {

        }

    where X implements java.lang.AutoCloseable, then "x" is a resource.
    """
    variable = property(attrgetter("_variable"))
    type = property(attrgetter("_type"))
    modifiers = property(attrgetter("_modifiers"))
    initializer = property(attrgetter("_initializer"))

    def serialize(self):
        initializer = ""
        if self.initializer is not None:
            initializer = " = " + self.initializer.serialize()

        return "{}{} {}{}".format(
            serialize_modifiers(self.modifiers),
            "" if self.type is None else self.type.serialize(),
            self.variable.serialize(),
            initializer
        )

    def __init__(self, variable, type_=None, modifiers=None,
                 initializer=None):
        super(Resource, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'initializer']

        self._variable = None
        self._type = None
        self._modifiers = None
        self._initializer = None

        self.variable = variable
        self.type = type_
        self.modifiers = modifiers
        self.initializer = initializer

    @variable.setter
    def variable(self, variable):
        self._variable = assert_type(variable, Variable)

    @type.setter
    def type(self, type_):
        self._type = assert_none_or(type_, Type)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @initializer.setter
    def initializer(self, initializer):
        self._initializer = assert_none_or(initializer, Expression)


class ConstructorInvocation(Statement):
    """
    An explicit invocations of a class's constructor.

    This is a variant of either this() or super(), NOT a "new" expression.
    """
    name = property(attrgetter("_name"))
    target = property(attrgetter("_target"))
    type_arguments = property(attrgetter("_type_arguments"))
    arguments = property(attrgetter("_arguments"))

    def __init__(self, name, target=None, type_arguments=None, arguments=None):
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'type_arguments', 'arguments']

        self._name = None
        self._target = None
        self._type_arguments = None
        self._arguments = None

        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @target.setter
    def target(self, target):
        self._target = assert_none_or(target, Expression)

    @type_arguments.setter
    def type_arguments(self, type_arguments):
        type_arguments = self._alter_tokens("type_arguments", type_arguments)
        self._type_arguments = self._assert_list_ensure(type_arguments, Type)

    @arguments.setter
    def arguments(self, arguments):
        arguments = self._alter_tokens("arguments", arguments)
        self._arguments = self._assert_list(arguments, Expression)

    def statement_serialize(self):
        target = ""
        if self.target is not None:
            target = self.target.serialize() + "."
        return "{}{}{}{};".format(
            target,
            serialize_type_arguments(self.type_arguments),
            self.name.serialize(),
            serialize_arguments(self.arguments)
        )


class ExpressionStatement(Statement):
    expression = property(attrgetter("_expression"))

    def __init__(self, expression):
        super(ExpressionStatement, self).__init__()
        self._fields = ['expression']

        self._expression = None

        self.expression = expression

    @expression.setter
    def expression(self, expression):
        self._expression = assert_type(expression, Expression)

    def statement_serialize(self):
        return self.expression.serialize() + ";"