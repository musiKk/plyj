class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class CompilationUnit(SourceElement):

    def __init__(self, package_declaration=None, import_declarations=[],
                 type_declarations=[]):
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations

    def __str__(self):
        return 'CompilationUnit[package_declaration={}, import_declarations={}, type_declarations={}]'.format(
                self.package_declaration, [str(i) for i in self.import_declarations], [str(t) for t in self.type_declarations])

class PackageDeclaration(SourceElement):

    def __init__(self, name, modifiers=[]):
        self.name = name
        self.modifiers = modifiers

    def __str__(self):
        return 'PackageDeclaration[name={}, modifiers={}]'.format(self.name, self.modifiers)

class ImportDeclaration(SourceElement):

    def __init__(self, name, static=False, on_demand=False):
        self.name = name
        self.static = static
        self.on_demand = on_demand

    def __str__(self):
        return 'ImportDeclaration[name={}, static={}, on_demand={}]'.format(
                self.name, self.static, self.on_demand)

class ClassDeclaration(SourceElement):

    def __init__(self, name, body, modifiers=[], type_parameters=[], extends=None, implements=[]):
        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements

    def __str__(self):
        return 'ClassDeclaration[name={}, modifiers={}, type_parameters={}, extends={}, implements={}, body={}]'.format(
                self.name, self.modifiers, self.type_parameters, self.extends, self.implements, [str(e) for e in self.body])

class ClassInitializer(SourceElement):

    def __init__(self, block, static=False):
        self.block = block
        self.static = static

    def __str__(self):
        return 'ClassInitializer[static={}, block={}]'.format(self.static, self.block)

class ConstructorDeclaration(SourceElement):

    def __init__(self, name, block, modifiers=[], type_parameters=[], parameters=[], throws=None):
        self.name = name
        self.block = block
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws

    def __str__(self):
        return 'ConstructorDeclaration[name={}, modifiers={}, type_parameters={}, parameters={}, throws={}, block={}]'.format(
                self.name, self.modifiers, self.type_parameters, self.parameters, self.throws, [str(e) for e in self.block])

class FieldDeclaration(SourceElement):

    def __init__(self, _type, variable_declarators, modifiers=[]):
        self._type = _type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers

    def __str__(self):
        return 'FieldDeclaration[type={}, modifiers={}, variable_declarators={}]'.format(
                self._type, self.modifiers, self.variable_declarators)

class MethodDeclaration(SourceElement):

    def __init__(self, name, modifiers=[], type_parameters=[], parameters=[], return_type='void', body=None, abstract=False, extended_dims=0, throws=None):
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.abstract = abstract
        self.extended_dims = extended_dims
        self.throws = throws

    def __str__(self):
        return 'MethodDeclaration[name={}, parameters={}, return_type={}, modifiers={}, type_parameters={}, abstract={}, throws={}, body={}]'.format(
                self.name, self.parameters, self.return_type, self.modifiers, self.type_parameters, self.abstract, self.throws, [str(s) for s in self.body])

class FormalParameter(SourceElement):

    def __init__(self, variable, _type, modifiers=[], vararg=False):
        self.variable = variable
        self._type = _type
        self.modifiers = modifiers
        self.vararg = vararg

    def __str__(self):
        return 'FormalParameter[variable={}, type={}, modifiers={}, vararg={}]'.format(
                self.variable, self._type, self.modifiers, self.vararg)

class Variable(SourceElement):
# I would like to remove this class. In theory, the dimension could be added to
# the type but this means variable declarations have to be changed somehow.
# Consider 'int i, j[];'. In this case there currently is only one type with two
# variable declarators; this closely resembles the source code. If the variable
# is to go away, the type has to be duplicated for every variable...

    def __init__(self, name, dimensions=0):
        self.name = name
        self.dimensions = dimensions

    def __str__(self):
        return 'Variable[name={}, dims={}]'.format(self.name, self.dimensions)

class VariableDeclarator(SourceElement):

    def __init__(self, variable, initializer=None):
        self.variable = variable
        self.initializer = initializer

    def __str__(self):
        return '{} = {}'.format(self.variable, self.initializer)

class Throws(SourceElement):

    def __init__(self, types):
        self.types = types

    def __str__(self):
        return 'Throws[types={}]'.format(self.types)

class InterfaceDeclaration(SourceElement):

    def __init__(self, name, modifiers=[], extends=[], type_parameters=[], body=[]):
        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body

    def __str__(self):
        return 'InterfaceDeclaration[name={}, modifiers={}, extends={}, type_parameters={}, body={}]'.format(
               self.name, self.modifiers, self.extends, self.type_parameters, self.body)

class EnumDeclaration(SourceElement):

    def __init__(self, name, implements=[], modifiers=[], type_parameters=[], body=[]):
        self.name = name
        self.implements = implements
        self.modifiers=modifiers
        self.type_parameters=type_parameters
        self.body = body

    def __str__(self):
        return 'EnumDeclaration[name={}, modifiers={}, implements={}, type_parameters={}, body={}]'.format(
               self.name, self.modifiers, self.implements, self.type_parameters, [str(e) for e in self.body])

class EnumConstant(SourceElement):

    def __init__(self, name, arguments=[], modifiers=[], body=[]):
        self.name = name
        self.arguments = arguments
        self.modifiers = modifiers
        self.body = body

    def __str__(self):
        return 'EnumConstant[name={}, arguments={}, modifiers={}, body={}]'.format(
               self.name, self.arguments, self.modifiers, [str(e) for e in self.body])

class AnnotationDeclaration(SourceElement):

    def __init__(self, name, modifiers=[], type_parameters=[], extends=None, implements=[], body=[]):
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body

    def __str__(self):
        return 'AnnotationDeclaration[name={}, modifiers={}, type_parameters={}, extends={}, implements={}, body={}]'.format(
               self.name, [str(m) for m in self.modifiers], self.type_parameters, self.extends, self.implements, [str(e) for e in self.body])

class AnnotationMethodDeclaration(SourceElement):

    def __init__(self, name, _type, parameters=[], default=None, modifiers=[], type_parameters=[], extended_dims=0):
        self.name = name
        self._type = _type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims

    def __str__(self):
        return 'AnnotationMethodDeclaration[name={}, type={}, parameters={}, default={}, modifiers={}, type_parameters={}]'.format(
               self.name, self._type, self.parameters, self.default, self.modifiers, self.type_parameters)

class Annotation(SourceElement):

    def __init__(self, name, members=[], single_member=None):
        self.name = name
        self.members = members
        self.single_member = single_member

    def __str__(self):
        return 'Annotation[name={}, members={}, single_member={}]'.format(self.name, [str(m) for m in self.members], self.single_member)

class AnnotationMember(SourceElement):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return 'AnnotationMember[name={}, value={}]'.format(self.name, self.value)

class ArrayInitializer(SourceElement):

    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return 'ArrayInitializer[elements={}]'.format(self.elements)

class Type(SourceElement):

    def __init__(self, name, type_arguments=[], enclosed_in=None, dimensions=0):
        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions

    def __str__(self):
        return 'Type[name={}, type_arguments={}, enclosed_in={}, dimensions={}]'.format(
               self.name, [str(t) for t in self.type_arguments], self.enclosed_in, self.dimensions)

class Wildcard(SourceElement):

    def __init__(self, bounds=[]):
        self.bounds = bounds

    def __str__(self):
        return 'Wildcard[bounds={}]'.format(self.bounds)

class WildcardBound(SourceElement):

    def __init__(self, _type, extends=False, _super=False):
        self._type = _type
        self.extends = extends
        self._super = _super

    def __str__(self):
        return 'WildcardBound[type={}, extends={}, super={}]'.format(self._type, self.extends, self._super)

class TypeParameter(SourceElement):

    def __init__(self, name, extends=[]):
        self.name = name
        self.extends = extends

    def __str__(self):
        return 'TypeParameter[name={}, extends={}]'.format(self.name, self.extends)

class Expression(SourceElement):
    pass

class BinaryExpression(Expression):

    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return '({}, {}, {})'.format(self.operator, self.lhs, self.rhs)

class Assignment(BinaryExpression):
    pass

class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false):
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false

    def __str__(self):
        return '(?:, {}, {}, {})'.format(self.predicate, self.if_true, self.if_false)

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
        self.sign = sign
        self.expression = expression

    def __str__(self):
        return '({}, {})'.format(self.sign, self.expression)

class Cast(Expression):

    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

    def __str__(self):
        return '(cast, {}, {})'.format(self.target, self.expression)

class Statement(SourceElement):
    pass

class Block(Statement):

    def __init__(self, statements=[]):
        self.statements = statements

    def __str__(self):
        return 'Block[statements={}]'.format([str(s) for s in self.statements])

    def __iter__(self):
        for s in self.statements:
            yield s

class VariableDeclaration(Statement, FieldDeclaration):

    def __str__(self):
        return 'VariableDeclaration[type={}, modifiers={}, variable_declarators={}]'.format(
               self._type, [str(m) for m in self.modifiers], [str(d) for d in self.variable_declarators])

class ArrayInitializer(SourceElement):

    def __init__(self, elements=[]):
        self.elements = elements

    def __str__(self):
        # '{' placeholder '}'
        return '{{{}}}'.format([str(e) for e in self.elements])

class MethodInvocation(Expression):

    def __init__(self, name, arguments=[], type_arguments=[], target=None):
        self.name = name
        self.arguments = arguments
        self.type_arguments = type_arguments
        self.target = target

    def __str__(self):
        return 'MethodInvocation[name={}, arguments={}, type_arguments={}, target={}]'.format(
               self.name, self.arguments, self.type_arguments, self.target)

class IfThenElse(Statement):

    def __init__(self, predicate, if_true=None, if_false=None):
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false

    def __str__(self):
        return 'if {} then {} else {}'.format(self.predicate, self.if_true, self.if_false)

class While(Statement):

    def __init__(self, predicate, body=None):
        self.predicate = predicate
        self.body = body

    def __str__(self):
        return 'while {} {}'.format(self.predicate, self.body)

class For(Statement):

    def __init__(self, init, predicate, update, body):
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body

    def __str__(self):
        return 'for {} {} {} {}'.format(self.init, self.predicate, self.update, self.body)

class ForEach(Statement):

    def __init__(self, _type, variable, iterable, body, modifiers=[]):
        self._type = _type
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers

    def __str__(self):
        return 'foreach ({} {} {} : {}) {}'.format(self.modifiers, self._type, self.variable, self.iterable, self.body)

class Assert(Statement):

    def __init__(self, predicate, message=None):
        self.predicate = predicate
        self.message = message

    def __str__(self):
        return 'assert({} : {})'.format(self.predicate, self.message)

class Switch(Statement):

    def __init__(self, expression, switch_cases):
        self.expression = expression
        self.switch_cases = switch_cases

    def __str__(self):
        return 'switch({}) {}'.format(self.expression, [str(s) for s in self.switch_cases])

class SwitchCase(SourceElement):

    def __init__(self, cases, body=[]):
        self.cases = cases
        self.body = body

    def __str__(self):
        return '{} {}'.format([str(c) for c in self.cases], [str(s) for s in self.body])

class DoWhile(Statement):

    def __init__(self, predicate, body=None):
        self.predicate = predicate
        self.body = body

    def __str__(self):
        return 'do {} while {}'.format(self.predicate, self.body)

class Continue(Statement):

    def __init__(self, label=None):
        self.label = label

    def __str__(self):
        return 'continue {}'.format(self.label)

class Break(Statement):

    def __init__(self, label=None):
        self.label = label

    def __str__(self):
        return 'break {}'.format(self.label)

class Return(Statement):

    def __init__(self, result=None):
        self.result = result

    def __str__(self):
        return 'return {}'.format(self.result)

class Synchronized(Statement):

    def __init__(self, monitor, body):
        self.monitor = monitor
        self.body = body

    def __str__(self):
        return 'synchronized {} {}'.format(self.monitor, self.body)

class Throw(Statement):

    def __init__(self, exception):
        self.exception = exception

    def __str__(self):
        return 'throw {}'.format(self.exception)

class Try(Statement):

    def __init__(self, block, catches=[], _finally=[], resources=[]):
        self.block = block
        self.catches = catches
        self._finally = _finally
        self.resources = resources

    def __str__(self):
        return 'try {} {} catch {} finally {}'.format([str(r) for r in self.resources], [str(e) for e in self.block], [str(c) for c in self.catches], [str(e) for e in self._finally])

class Catch(SourceElement):

    def __init__(self, variable, modifiers=[], types=[], block=[]):
        self.variable = variable
        self.modifiers = modifiers
        self.types = types
        self.block = block

    def __str__(self):
        return 'catch {} {} {} {}'.format(self.modifiers, [str(t) for t in self.types], self.variable, [str(e) for e in self.block])

class Resource(SourceElement):

    def __init__(self, variable, _type=None, modifiers=[], initializer=None):
        self.variable = variable
        self._type = _type
        self.modifiers = modifiers
        self.initializer = initializer

    def __str__(self):
        return 'resource {} {} {} {}'.format(self.modifiers, self._type, self.variable, self.initializer)

class ConstructorInvocation(Statement):
    """An explicit invocations of a class's constructor.

    This is a variant of either this() or super(), NOT a "new" expression.
    """

    def __init__(self, name, target=None, type_arguments=[], arguments=[]):
        """Arguments:

        name - either "super" or "this"
        """
        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments

    def __str__(self):
        return 'ConstructorInvocation[name={}, target={}, type_arguments={}, arguments={}]'.format(
               self.name, self.target, self.type_arguments, self.arguments)

class InstanceCreation(Expression):

    def __init__(self, _type, type_arguments=[], arguments=[], body=[], enclosed_in=None):
        self._type = _type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in

    def __str__(self):
        return 'InstanceCreation[type={}, type_arguments={}, enclosed_in={}, arguments={}, body={}]'.format(
               self._type, self.type_arguments, self.enclosed_in, self.arguments, self.body)

class FieldAccess(Expression):

    def __init__(self, name, target):
        self.name = name
        self.target = target

    def __str__(self):
        return 'FieldAccess[name={}, target={}]'.format(self.name, self.target)

class ArrayAccess(Expression):

    def __init__(self, index, target):
        self.index = index
        self.target = target

    def __str__(self):
        return 'ArrayAccess[index={}, target={}]'.format(self.index, self.target)

class ArrayCreation(Expression):

    def __init__(self, _type, dimensions=[], initializer=None):
        self._type = _type
        self.dimensions = dimensions
        self.initializer = initializer

    def __str__(self):
        return 'ArrayCreation[type={}, dimensions={}, initializer={}]'.format(
               self._type, self.dimensions, self.initializer)

class Literal(SourceElement):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Literal[{}]'.format(self.value)

class Name(SourceElement):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Name[{}]'.format(self.value)
