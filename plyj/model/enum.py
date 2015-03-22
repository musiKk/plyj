#!/usr/bin/env python2
from operator import attrgetter
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.source_element import SourceElement, Declaration, Modifier, \
    Expression
from plyj.model.type import Type, TypeParameter
from plyj.utility import serialize_body, serialize_implements, \
    serialize_type_parameters, serialize_modifiers, indent


class EnumDeclaration(Declaration):
    name = property(attrgetter("_name"))
    implements = property(attrgetter("_implements"))
    modifiers = property(attrgetter("_modifiers"))
    type_parameters = property(attrgetter("_type_parameters"))
    body = property(attrgetter("_body"))

    def __init__(self, name, implements=None, modifiers=None,
                 type_parameters=None, body=None):
        super(EnumDeclaration, self).__init__()
        self._fields = ['name', 'implements', 'modifiers', 'type_parameters',
                        'body']

        self._name = None
        self._body = None
        self._implements = None
        self._modifiers = None
        self._type_parameters = None

        self.name = name
        self.body = body
        self.implements = implements
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.body = body

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @body.setter
    def body(self, body):
        body = self._alter_tokens("body", body)
        self._body = self._assert_list(body, (EnumConstant, Declaration))

        in_declarations = False
        for i, declaration in enumerate(self.body):
            if isinstance(declaration, Declaration):
                if not in_declarations:
                    in_declarations = True
            else:
                # If we're here, this must be an EnumConstant, which CANNOT
                # appear after a declaration
                assert not in_declarations

    @implements.setter
    def implements(self, implements):
        self._implements = self._assert_list(implements, Type)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @type_parameters.setter
    def type_parameters(self, type_parameters):
        self._type_parameters = self._assert_list(type_parameters,
                                                  TypeParameter)

    def serialize(self):
        body = ""
        in_declarations = False
        for x in self.body:
            if isinstance(x, Declaration):
                if not in_declarations:
                    in_declarations = True
                    body = body[0:-2]  # Remove trailing ",\n"
                    body += ";\n"
                body += x.serialize() + "\n"
            else:
                body += x.serialize() + ",\n"
        body = indent(body)
        return "{}enum {}{} {}{{\n{}}}".format(
            serialize_modifiers(self.modifiers),
            self.name.serialize(),
            serialize_type_parameters(self.type_parameters),
            serialize_implements(self.implements),
            body
        )


class EnumConstant(SourceElement):
    name = property(attrgetter("_name"))
    arguments = property(attrgetter("_arguments"))
    modifiers = property(attrgetter("_modifiers"))
    body = property(attrgetter("_body"))

    def __init__(self, name, arguments=None, modifiers=None, body=None):
        super(EnumConstant, self).__init__()
        self._fields = ['name', 'arguments', 'modifiers', 'body']

        self._name = None
        self._arguments = None
        self._modifiers = None
        self._body = None

        self.name = name
        self.arguments = arguments
        self.modifiers = modifiers
        self.body = body

    @name.setter
    def name(self, name):
        self._name = Name.ensure(name, True)

    @arguments.setter
    def arguments(self, arguments):
        self._arguments = self._assert_list(arguments, Expression)

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = self._assert_list(modifiers, Modifier,
                                            BasicModifier.ensure_modifier)

    @body.setter
    def body(self, body):
        self._body = self._assert_list(body, Declaration)

    def serialize(self):
        if len(self.arguments) == 0:
            arguments = ""
        else:
            arguments = [x.serialize() for x in self.arguments]
            arguments = "(" + ", ".join(arguments) + ")"
        body = serialize_body(self.body, "")
        if len(body) > 0:
            body = " " + body
        return "{}{}{}{}".format(
            serialize_modifiers(self.modifiers),
            self.name.serialize(),
            arguments,
            body,
        )