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
    serialize_arguments


class Empty(Statement):
    def statement_serialize(self):
        return ""


class Block(Statement):
    statements = property(attrgetter("_statements"))

    def statement_serialize(self):
        """
        result = "{\n"
        for statement in self.statements:
            result += "    " + statement.serialize() + ";\n"
        result += "}"
        return result
        """
        return serialize_body(self.statements)

    def __init__(self, statements=None):
        super(Statement, self).__init__()
        self._fields = ['statements']

        self._statements = self._assert_body(statements)

    def __iter__(self):
        for s in self._statements:
            yield s


class VariableDeclaration(Declaration):
    type = property(attrgetter("_type"))
    variable_declarators = property(attrgetter("_variable_declarators"))
    modifiers = property(attrgetter("_modifiers"))

    def statement_serialize(self):
        result = serialize_modifiers(self.modifiers)
        result += self.type.serialize()
        result += ", ".join([x.serialize() for x in self.variable_declarators])
        return result

    def __init__(self, type_, variable_declarators, modifiers=None):
        super(VariableDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']

        variable_declarators = self._absorb_ase_tokens(variable_declarators)

        self._type = Type.ensure(type_)
        self._variable_declarators = self._assert_list(variable_declarators,
                                                       VariableDeclarator)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)


class VariableDeclarationStatement(VariableDeclaration, Statement):
    pass


class IfThenElse(Statement):
    predicate = property(attrgetter("_predicate"))
    if_true = property(attrgetter("_if_true"))
    if_false = property(attrgetter("_if_false"))

    def statement_serialize(self):
        if self.if_false is None:
            return "if ({}) {}".format(self.predicate.serialize(),
                                       self.if_true.serialize())
        else:
            return "if ({}) {}\n else {}".format(self.predicate.serialize(),
                                                 self.if_true.serialize(),
                                                 self.if_false.serialize())

    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']

        self._predicate = assert_type(predicate, Expression)
        self._if_true = assert_none_or(if_true, Statement)
        self._if_false = assert_none_or(if_false, Statement)


class While(Statement):
    predicate = property(attrgetter("_predicate"))
    body = property(attrgetter("_body"))

    def statement_serialize(self):
        return "while ({}) {}".format(self.predicate.serialize(),
                                      self.body.serialize())

    def __init__(self, predicate, body=None):
        super(While, self).__init__()
        self._fields = ['predicate', 'body']

        self._predicate = assert_type(predicate, Expression)
        self._body = assert_none_or(body, Statement)


class For(Statement):
    init = property(attrgetter("_init"))
    predicate = property(attrgetter("_predicate"))
    update = property(attrgetter("_update"))
    body = property(attrgetter("_body"))

    def statement_serialize(self):
        return "for ({};{};{}) {}".format(self.init.serialize(),
                                          self.predicate.serialize(),
                                          self.update.serialize(),
                                          self.body.serialize())

    def __init__(self, init, predicate, update, body):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body']

        self._init = self._assert_list(init, (Expression,
                                              VariableDeclarationStatement))
        self._predicate = assert_none_or(predicate, Expression)
        self._update = self._assert_list(update, Expression)
        self._body = assert_type(body, Statement)


class ForEach(Statement):
    type = property(attrgetter("_type"))
    variable = property(attrgetter("_variable"))
    iterable = property(attrgetter("_iterable"))
    body = property(attrgetter("_body"))
    modifiers = property(attrgetter("_modifiers"))

    def statement_serialize(self):
        return "for ({}{} {} : {}) {}".format(
            serialize_modifiers(self.modifiers),
            self.type.serialize(),
            self.variable.serialize(),
            self.iterable.serialize(),
            self.body.serialize()
        )

    def __init__(self, type_, variable, iterable, body, modifiers=None):
        super(ForEach, self).__init__()
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers']

        self._type = Type.ensure(type_)
        self._variable = assert_type(variable, Variable)
        self._iterable = assert_type(iterable, Expression)
        self._body = assert_type(body, Statement)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)


class Assert(Statement):
    predicate = property(attrgetter("_predicate"))
    message = property(attrgetter("_message"))

    def statement_serialize(self):
        return "assert {}{}".format(
            self.predicate.serialize(),
            "" if self.message is None else ", " + self.message.serialize(),
        )

    def __init__(self, predicate, message=None):
        super(Assert, self).__init__()
        self._fields = ['predicate', 'message']

        self._predicate = assert_type(predicate, Expression)
        self._message = assert_none_or(message, Expression)


class Switch(Statement):
    expression = property(attrgetter("_expression"))
    switch_cases = property(attrgetter("_switch_cases"))

    def statement_serialize(self):
        return "switch ({}) {{\n{}\n}}\n".format(
            self.expression.serialize(),
            "".join([x.serialize() for x in self.switch_cases])
        )

    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases']

        self._expression = assert_type(expression, Expression)
        self._switch_cases = self._assert_list(switch_cases, SwitchCase)


class SwitchCase(SourceElement):
    cases = property(attrgetter("_cases"))
    body = property(attrgetter("_body"))
    default = property(attrgetter("_default"))

    def statement_serialize(self):
        result = ""
        if self.default:
            result += "default:\n"
        else:
            for case in self.cases:
                result += "case " + case.serialize() + ":\n"
        result += serialize_body(self.body)

    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body']

        default = False
        for i, c in enumerate(cases):
            if (c == "default" or
               (isinstance(c, Name) and c.value == "default") or
               (isinstance(c, AnonymousSE) and c.value == "default")):
                default = True
                del cases[i]
                break

        self._cases = self._assert_list(cases, Expression)
        self._body = self._assert_body(body)
        self._default = default


class DoWhile(Statement):
    predicate = property(attrgetter("_predicate"))
    body = property(attrgetter("_body"))

    def statement_serialize(self):
        return ("do " + self.body.serialize() + " while(" +
                self.predicate.serialize() + ")")

    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body']

        self._predicate = assert_type(predicate, Expression)
        self._body = assert_none_or(body, Statement)


class Continue(Statement):
    label = property(attrgetter("_label"))

    def statement_serialize(self):
        if self.label is None:
            return "continue"
        else:
            return "continue " + self.label.serialize()

    def __init__(self, label=None):
        super(Continue, self).__init__()
        self._fields = ['label']

        self._label = assert_none_or_ensure(label, Name, True)


class Break(Statement):
    label = property(attrgetter("_label"))

    def statement_serialize(self):
        if self.label is None:
            return "break"
        else:
            return "break " + self.label.serialize()

    def __init__(self, label=None):
        super(Break, self).__init__()
        self._fields = ['label']

        self._label = assert_none_or_ensure(label, Name, True)


class Return(Statement):
    result = property(attrgetter("_result"))

    def statement_serialize(self):
        if self.result is None:
            return "return"
        else:
            return "return " + self.result.serialize()

    def __init__(self, result=None):
        super(Return, self).__init__()
        self._fields = ['result']

        self._result = assert_none_or(result, Expression)


class Synchronized(Statement):
    monitor = property(attrgetter("_monitor"))
    body = property(attrgetter("_body"))

    def statement_serialize(self):
        return ("synchronized (" + self.monitor.serialize() + ") " +
                self.body.serialize())

    def __init__(self, monitor, body):
        super(Synchronized, self).__init__()
        self._fields = ['monitor', 'body']

        self._monitor = assert_type(monitor, Expression)
        self._body = self._assert_list(body, Statement)


class Throw(Statement):
    exception = property(attrgetter("_exception"))

    def statement_serialize(self):
        return "throw " + self.exception.serialize()

    def __init__(self, exception):
        super(Throw, self).__init__()
        self._fields = ['exception']

        self._exception = assert_type(exception, Expression)


class Try(Statement):
    block = property(attrgetter("_block"))
    catches = property(attrgetter("_catches"))
    finally_ = property(attrgetter("_finally"))
    resources = property(attrgetter("_resources"))

    def statement_serialize(self):
        result = "try "
        if self.resources is not None:
            resources = [x.serialize() for x in self.resources]
            result += "(" + ";".join(resources) + ")"
        result += self.block.serialize()
        result += "".join([x.serialize() + "\n" for x in self.catches])
        if self.finally_ is not None:
            result += self.finally_.serialize()

    def __init__(self, block, catches=None, finally_=None, resources=None):
        super(Try, self).__init__()
        self._fields = ['block', 'catches', 'finally_', 'resources']

        self._block = assert_type(block, Block)
        self._catches = self._assert_list(catches, Catch)
        self._finally = assert_none_or(finally_, Block)
        self._resources = self._assert_list(resources, Resource)

    def accept(self, visitor):
        if visitor.visit_Try(self):
            for s in self.block:
                s.accept(visitor)
        for c in self.catches:
            visitor.visit_Catch(c)
        if self._finally:
            self._finally.accept(visitor)


class Catch(SourceElement):
    variable = property(attrgetter("_variable"))
    modifiers = property(attrgetter("_modifiers"))
    types = property(attrgetter("_types"))
    block = property(attrgetter("_block"))

    def statement_serialize(self):
        result = "catch (" + serialize_modifiers(self.modifiers)
        result += " | ".join([x.serialize() for x in self.types])
        result += self.variable.serialize()
        result += ") " + self.block.serialize()
        return result

    def __init__(self, variable, modifiers=None, types=None, block=None):
        super(Catch, self).__init__()
        self._fields = ['variable', 'modifiers', 'types', 'block']

        self._variable = assert_type(variable, Variable)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
        self._types = self._assert_list_ensure(types, Type)
        self._block = assert_none_or(block, Block)


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

    def statement_serialize(self):
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

        self._variable = assert_type(variable, Variable)
        self._type = assert_none_or(type_, Type)
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)
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

    def statement_serialize(self):
        target = ""
        if self.target is not None:
            target = self.target.serialize() + "."
        return "{}{}{}{}".format(
            target,
            self.name.serialize(),
            serialize_type_arguments(self.type_arguments),
            serialize_arguments(self.arguments)
        )

        return "{}{} {}{}".format(
            serialize_modifiers(self.modifiers),
            "" if self.type is None else self.type.serialize(),
            self.variable.serialize(),
            initializer
        )

    def __init__(self, name, target=None, type_arguments=None, arguments=None):
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'type_arguments', 'arguments']

        arguments = self._absorb_ase_tokens(arguments)
        type_arguments = self._absorb_ase_tokens(type_arguments)

        self._name = Name.ensure(name, True)
        self._target = assert_none_or(target, Expression)
        self._type_arguments = self._assert_list_ensure(type_arguments, Type)
        self._arguments = self._assert_list(arguments, Expression)


class ExpressionStatement(Statement):
    expression = property(attrgetter("_expression"))

    def statement_serialize(self):
        return self.expression.serialize()

    def __init__(self, expression):
        super(ExpressionStatement, self).__init__()
        self._fields = ['expression']

        self._expression = assert_type(expression, Expression)