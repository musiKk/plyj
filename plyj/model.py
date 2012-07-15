class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''
    pass

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
                self.name, self.parameters, self.return_type, self.modifiers, self.type_parameters, self.abstract, self.throws, self.body)

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

    def __init__(self, name, dimensions=0):
        self.name = name
        self.dimensions = dimensions

    def __str__(self):
        return 'Variable[name={}, dims={}]'.format(self.name, self.dimensions)

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
