# Base node
class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        pass


class CompilationUnit(SourceElement):

    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = [
            'package_declaration', 'import_declarations', 'type_declarations']
        if import_declarations is None:
            import_declarations = []
        if type_declarations is None:
            type_declarations = []
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations

    def accept(self, visitor):
        if visitor.visit_CompilationUnit(self):
            if self.package_declaration:
                self.package_declaration.accept(visitor)
            for import_decl in self.import_declarations:
                import_decl.accept(visitor)
            for type_decl in self.type_declarations:
                type_decl.accept(visitor)


class PackageDeclaration(SourceElement):

    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.name = name
        self.modifiers = modifiers

    def accept(self, visitor):
        visitor.visit_PackageDeclaration(self)


class ImportDeclaration(SourceElement):

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']
        self.name = name
        self.static = static
        self.on_demand = on_demand

    def accept(self, visitor):
        visitor.visit_ImportDeclaration(self)


class ClassDeclaration(SourceElement):

    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None):
        super(ClassDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements

    def accept(self, visitor):
        if visitor.visit_ClassDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class ClassInitializer(SourceElement):

    def __init__(self, block, static=False):
        super(ClassInitializer, self).__init__()
        self._fields = ['block', 'static']
        self.block = block
        self.static = static

    def accept(self, visitor):
        if visitor.visit_ClassInitializer(self):
            for expr in self.block:
                expr.accept(visitor)


class ConstructorDeclaration(SourceElement):

    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'block', 'modifiers',
                        'type_parameters', 'parameters', 'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.block = block
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws

    def accept(self, visitor):
        if visitor.visit_ConrepructorDeclaration(self):
            for expr in self.block:
                expr.accept(visitor)


class FieldDeclaration(SourceElement):

    def __init__(self, type, variable_declarators, modifiers=None):
        super(FieldDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers

    def accept(self, visitor):
        visitor.visit_FieldDeclaration(self)


class MethodDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None,
                 parameters=None, returntype='void', body=None, abrepract=False,
                 extended_dims=0, throws=None):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'type_parameters', 'parameters',
                        'returntype', 'body', 'abrepract', 'extended_dims',
                        'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.returntype = returntype
        self.body = body
        self.abrepract = abrepract
        self.extended_dims = extended_dims
        self.throws = throws

    def accept(self, visitor):
        if visitor.visit_MethodDeclaration(self):
            for e in self.body:
                e.accept(visitor)


class FormalParameter(SourceElement):

    def __init__(self, variable, type, modifiers=None, vararg=False):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.vararg = vararg


class Variable(SourceElement):
    # I would like to remove this class. In theory, the dimension could be added
    # to the type but this means variable declarations have to be changed
    # somehow. Consider 'int i, j[];'. In this case there currently is only one
    # type with two variable declarators;This closely resembles the source code.
    # If the variable is to go away, the type has to be duplicated for every
    # variable...

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions


class VariableDeclarator(SourceElement):

    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']
        self.variable = variable
        self.initializer = initializer


class Throws(SourceElement):

    def __init__(self, types):
        super(Throws, self).__init__()
        self._fields = ['types']
        self.types = types


class InterfaceDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, extends=None, type_parameters=None,
                 body=None):
        super(InterfaceDeclaration, self).__init__()
        self._fields = [
            'name', 'modifiers', 'extends', 'type_parameters', 'body']
        if modifiers is None:
            modifiers = []
        if extends is None:
            extends = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body

    def accept(self, visitor):
        if visitor.visit_InterfaceDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class EnumDeclaration(SourceElement):

    def __init__(self, name, implements=None, modifiers=None,
                 type_parameters=None, body=None):
        super(EnumDeclaration, self).__init__()
        self._fields = [
            'name', 'implements', 'modifiers', 'type_parameters', 'body']
        if implements is None:
            implements = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.implements = implements
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.body = body

    def accept(self, visitor):
        if visitor.visit_EnumDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class EnumConstant(SourceElement):

    def __init__(self, name, arguments=None, modifiers=None, body=None):
        super(EnumConstant, self).__init__()
        self._fields = ['name', 'arguments', 'modifiers', 'body']
        if arguments is None:
            arguments = []
        if modifiers is None:
            modifiers = []
        if body is None:
            body = []
        self.name = name
        self.arguments = arguments
        self.modifiers = modifiers
        self.body = body

    def accept(self, visitor):
        if visitor.visit_EnumConstant(self):
            for expr in self.body:
                expr.accept(visitor)


class AnnotationDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None, extends=None,
                 implements=None, body=None):
        super(AnnotationDeclaration, self).__init__()
        self._fields = [
            'name', 'modifiers', 'type_parameters', 'extends', 'implements',
            'body']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body

    def accept(self, visitor):
        if visitor.visit_AnnotationDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class AnnotationMethodDeclaration(SourceElement):

    def __init__(self, name, type, parameters=None, default=None,
                 modifiers=None, type_parameters=None, extended_dims=0):
        super(AnnotationMethodDeclaration, self).__init__()
        self._fields = ['name', 'type', 'parameters', 'default',
                        'modifiers', 'type_parameters', 'extended_dims']
        if parameters is None:
            parameters = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        self.name = name
        self.type = type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims

    def accept(self, visitor):
        visitor.visit_AnnotationMethodDeclaration(self)


class Annotation(SourceElement):

    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member']
        if members is None:
            members = []
        self.name = name
        self.members = members
        self.single_member = single_member


class AnnotationMember(SourceElement):

    def __init__(self, name, value):
        super(SourceElement, self).__init__()
        self._fields = ['name', 'value']
        self.name = name
        self.value = value


class Type(SourceElement):

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions


class Wildcard(SourceElement):

    def __init__(self, bounds=None):
        super(Wildcard, self).__init__()
        self._fields = ['bounds']
        if bounds is None:
            bounds = []
        self.bounds = bounds


class WildcardBound(SourceElement):

    def __init__(self, type, extends=False, _super=False):
        super(WildcardBound, self).__init__()
        self._fields = ['type', 'extends', '_super']
        self.type = type
        self.extends = extends
        self._super = _super


class TypeParameter(SourceElement):

    def __init__(self, name, extends=None):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends']
        if extends is None:
            extends = []
        self.name = name
        self.extends = extends


class Expression(SourceElement):

    def __init__(self):
        super(Expression, self).__init__()
        self._fields = []

    def accept(self, visitor):
        visitor.visit_Expression(self)


class BinaryExpression(Expression):

    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def accept(self, visitor):
        if visitor.visit_BinaryExpression(self):
            self.lhs.accept(visitor)
            self.rhs.accept(visitor)


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


class Statement(SourceElement):
    pass


class Block(Statement):

    def __init__(self, statements=None):
        super(Statement, self).__init__()
        self._fields = ['statements']
        if statements is None:
            statements = []
        self.statements = statements

    def __iter__(self):
        for s in self.statements:
            yield s

    def accept(self, visitor):
        if visitor.visit_Block(self):
            [s.accept(visitor) for s in self.statements]


class VariableDeclaration(Statement, FieldDeclaration):
    def accept(self, visitor):
        visitor.visit_VariableDeclaration(self)


class ArrayInitializer(SourceElement):
    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']
        if elements is None:
            elements = []
        self.elements = elements


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

    def accept(self, visitor):
        visitor.visit_MethodInvocation(self)


class IfThenElse(Statement):

    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false

    def accept(self, visitor):
        visitor.visit_IfThenElse(self)


class While(Statement):

    def __init__(self, predicate, body=None):
        super(While, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body

    def accept(self, visitor):
        visitor.visit_While(self)


class For(Statement):

    def __init__(self, init, predicate, update, body):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body']
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body

    def accept(self, visitor):
        if visitor.visit_For(self):
            self.body.accept(visitor)


class ForEach(Statement):

    def __init__(self, type, variable, iterable, body, modifiers=None):
        super(ForEach, self).__init__()
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers

    def accept(self, visitor):
        if visitor.visit_ForEach(self):
            self.body.accept(visitor)


class Assert(Statement):

    def __init__(self, predicate, message=None):
        super(Assert, self).__init__()
        self._fields = ['predicate', 'message']
        self.predicate = predicate
        self.message = message

    def accept(self, visitor):
        visitor.visit_Assert(self)


class Switch(Statement):

    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases']
        self.expression = expression
        self.switch_cases = switch_cases

    def accept(self, visitor):
        if visitor.visit_Switch(self):
            for s in self.switch_cases:
                s.accept(visitor)


class SwitchCase(SourceElement):

    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body']
        if body is None:
            body = []
        self.cases = cases
        self.body = body

    def accept(self, visitor):
        if visitor.visit_SwitchCase(self):
            for s in self.body:
                s.accept(visitor)


class DoWhile(Statement):

    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body

    def accept(self, visitor):
        if visitor.visit_DoWhile(self):
            self.body.accept(visitor)


class Continue(Statement):

    def __init__(self, label=None):
        super(Continue, self).__init__()
        self._fields = ['label']
        self.label = label

    def accept(self, visitor):
        visitor.visit_Continue(self)


class Break(Statement):

    def __init__(self, label=None):
        super(Break, self).__init__()
        self._fields = ['label']
        self.label = label

    def accept(self, visitor):
        visitor.visit_Break(self)


class Return(Statement):

    def __init__(self, result=None):
        super(Return, self).__init__()
        self._fields = ['result']
        self.result = result

    def accept(self, visitor):
        visitor.visit_Return(self)


class Synchronized(Statement):

    def __init__(self, monitor, body):
        super(Synchronized, self).__init__()
        self._fields = ['monitor', 'body']
        self.monitor = monitor
        self.body = body

    def accept(self, visitor):
        if visitor.visit_Synchronized(self):
            for s in self.body:
                s.accept(visitor)


class Throw(Statement):

    def __init__(self, exception):
        super(Throw, self).__init__()
        self._fields = ['exception']
        self.exception = exception

    def accept(self, visitor):
        visitor.visit_Throw(self)


class Try(Statement):

    def __init__(self, block, catches=None, _finally=None, resources=None):
        super(Try, self).__init__()
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
        super(Catch, self).__init__()
        self._fields = ['variable', 'modifiers', 'types', 'block']
        if modifiers is None:
            modifiers = []
        if types is None:
            types = []
        self.variable = variable
        self.modifiers = modifiers
        self.types = types
        self.block = block

    def accept(self, visitor):
        if visitor.visit_Catch(self):
            self.block.accept(visitor)


class Resource(SourceElement):

    def __init__(self, variable, type=None, modifiers=None, initializer=None):
        super(Resource, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'initializer']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.initializer = initializer


class ConstructorInvocation(Statement):
    """An explicit invocations of a class's conrepructor.

    This is a variant of either this() or super(), NOT a "new" expression.
    """

    def __init__(self, name, target=None, type_arguments=None, arguments=None):
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'type_arguments', 'arguments']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments

    def accept(self, visitor):
        visitor.visit_ConrepructorInvocation(self)


class InstanceCreation(Expression):

    def __init__(self, type, type_arguments=None, arguments=None, body=None,
                 enclosed_in=None):
        super(InstanceCreation, self).__init__()
        self._fields = [
            'type', 'type_arguments', 'arguments', 'body', 'enclosed_in']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in

    def accept(self, visitor):
        visitor.visit_InstanceCreation(self)


class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target']
        self.name = name
        self.target = target

    def accept(self, visitor):
        visitor.visit_FieldAccess(self)


class ArrayAccess(Expression):

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']
        self.index = index
        self.target = target

    def accept(self, visitor):
        visitor.visit_ArrayAccess(self)


class ArrayCreation(Expression):

    def __init__(self, type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']
        if dimensions is None:
            dimensions = []
        self.type = type
        self.dimensions = dimensions
        self.initializer = initializer

    def accept(self, visitor):
        visitor.visit_ArrayCreation(self)


class Literal(SourceElement):

    def __init__(self, value):
        super(Literal, self).__init__()
        self._fields = ['value']
        self.value = value

    def accept(self, visitor):
        visitor.visit_Literal(self)


class ClassLiteral(SourceElement):

    def __init__(self, type):
        super(ClassLiteral, self).__init__()
        self._fields = ['type']
        self.type = type


class Name(SourceElement):

    def __init__(self, value):
        super(Name, self).__init__()
        self._fields = ['value']
        self.value = value

    def append_name(self, name):
        try:
            self.value = self.value + '.' + name.value
        except:
            self.value = self.value + '.' + name

    def accept(self, visitor):
        visitor.visit_Name(self)


class Visitor(object):
    def __getattr__(self, name):
        if not name.startswith('visit_'):
            raise AttributeError('name must start with visit_ but was {}'
                                 .format(name))

        def f(element):
            if self.verbose:
                msg = 'unimplemented call to {}; ignoring ({})'
                print(msg.format(name, element))
            return True
        return f
