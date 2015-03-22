#!/usr/bin/env python2

import sys
from plyj.parser import Parser
import plyj.visitor as m

p = Parser()
tree = p.parse_file(sys.argv[1])


class MyVisitor(m.Visitor):
    def __init__(self):
        super(MyVisitor, self).__init__()

        self.first_field = True
        self.first_method = True

    def visit_ClassDeclaration(self, class_decl):
        return self.visit_type_declaration(class_decl)

    def visit_InterfaceDeclaration(self, interface_decl):
        return self.visit_type_declaration(interface_decl)

    def visit_type_declaration(self, type_decl):
        print(str(type_decl.name))
        if type_decl.extends is not None:
            print(' -> extending ' + type_decl.extends.name.value)
        if len(type_decl.implements) is not 0:
            print(' -> implementing ' + ', '.join([type.name.value for type in type_decl.implements]))
        print

        return True

    def visit_FieldDeclaration(self, field_decl):
        if self.first_field:
            print('fields:')
            self.first_field = False
        for var_decl in field_decl.variable_declarators:
            if type(field_decl.type) is str:
                type_name = field_decl.type.serialize()
            else:
                type_name = field_decl.type.name.serialize()
            print('    ' + type_name + ' ' + var_decl.variable.name.serialize())

    def visit_MethodDeclaration(self, method_decl):
        if self.first_method:
            print
            print('methods:')
            self.first_method = False

        param_strings = []
        for param in method_decl.parameters:
            if type(param.type) is str:
                param_strings.append(param.type.serialize() + ' ' + param.variable.serialize())
            else:
                param_strings.append(param.type.name.serialize() + ' ' + param.variable.name.serialize())
        print('    ' + method_decl.name.serialize() + '(' + ', '.join(param_strings) + ')')

        return True

    def visit_VariableDeclaration(self, var_declaration):
        for var_decl in var_declaration.variable_declarators:
            if type(var_declaration.type) is str:
                type_name = var_declaration.type.serialize()
            else:
                type_name = var_declaration.type.name.serialize()
            print('        ' + type_name + ' ' + var_decl.variable.name.serialize())

print('declared types:')
tree.accept(MyVisitor())
