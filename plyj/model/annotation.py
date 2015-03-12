#!/usr/bin/env python2
from plyj.model.expression import Expression
from plyj.model.name import Name, ensure_name
from plyj.model.source_element import SourceElement, AnonymousSourceElement, \
    ensure_se, extract_tokens, Expression
from plyj.model.type import Type


class Annotation(SourceElement):
    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member']
        if members is None:
            members = []

        name = ensure_name(name, True)
        members = extract_tokens(self, members)

        assert isinstance(members, list)
        assert (single_member is None or
                isinstance(single_member, AnnotationMember))

        self.name = name
        self.members = members
        self.single_member = single_member


class AnnotationMethodDeclaration(SourceElement):
    def __init__(self, name, return_type, parameters=None, default=None,
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

        name = ensure_name(name, True)
        extended_dims = ensure_se(extended_dims)

        assert isinstance(return_type, Type)
        assert isinstance(parameters, list)
        assert isinstance(default, Expression)
        assert isinstance(modifiers, list)
        assert isinstance(type_parameters, list)
        assert isinstance(extended_dims, AnonymousSourceElement)

        self.name = name
        self.type = return_type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims


class AnnotationMember(SourceElement):
    def __init__(self, name, value):
        super(AnnotationMember, self).__init__()
        self._fields = ['name', 'value']

        name = ensure_name(name)
        assert isinstance(value, SourceElement)

        self.name = name
        self.value = value


class AnnotationDeclaration(SourceElement):
    def __init__(self, name, modifiers=None, type_parameters=None,
                 extends=None, implements=None, body=None):
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

        name = ensure_name(name, True)
        assert extends is None or isinstance(extends, Type)
        assert isinstance(implements, list)
        assert isinstance(body, list)
        assert isinstance(modifiers, list)
        assert isinstance(type_parameters, list)

        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body