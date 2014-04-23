#!/usr/bin/env python2

import sys
import plyj.parser
import plyj.model as m

p = plyj.parser.Parser()
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
                type_name = field_decl.type
            else:
                type_name = field_decl.type.name.value
            print('    ' + type_name + ' ' + var_decl.variable.name)

    def visit_MethodDeclaration(self, method_decl):
        if self.first_method:
            print
            print('methods:')
            self.first_method = False

        param_strings = []
        for param in method_decl.parameters:
            if type(param.type) is str:
                param_strings.append(param.type + ' ' + param.variable.name)
            else:
                param_strings.append(param.type.name.value + ' ' + param.variable.name)
        print('    ' + method_decl.name + '(' + ', '.join(param_strings) + ')')

        return True

    def visit_VariableDeclaration(self, var_declaration):
        for var_decl in var_declaration.variable_declarators:
            if type(var_declaration.type) is str:
                type_name = var_declaration.type
            else:
                type_name = var_declaration.type.name.value
            print('        ' + type_name + ' ' + var_decl.variable.name)

print('declared types:')
tree.accept(MyVisitor())
