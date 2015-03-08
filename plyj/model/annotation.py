#!/usr/bin/env python2
from plyj.model.source_element import SourceElement


class Annotation(SourceElement):
    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member']
        if members is None:
            members = []
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
        self.name = name
        self.type = return_type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims


class AnnotationMember(SourceElement):
    def __init__(self, name, value):
        super(SourceElement, self).__init__()
        self._fields = ['name', 'value']
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
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body