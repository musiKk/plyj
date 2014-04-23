#!/usr/bin/env python2

import sys
import plyj.parser
import plyj.model as m

p = plyj.parser.Parser()
tree = p.parse_file(sys.argv[1])

print('declared types:')
for type_decl in tree.type_declarations:
    print(type_decl.name)
    if type_decl.extends is not None:
        print(' -> extending ' + type_decl.extends.name.value)
    if len(type_decl.implements) is not 0:
        print(' -> implementing ' + ', '.join([type.name.value for type in type_decl.implements]))
    print

    print('fields:')
    for field_decl in [decl for decl in type_decl.body if type(decl) is m.FieldDeclaration]:
        for var_decl in field_decl.variable_declarators:
            if type(field_decl.type) is str:
                type_name = field_decl.type
            else:
                type_name = field_decl.type.name.value
            print('    ' + type_name + ' ' + var_decl.variable.name)

    print
    print('methods:')
    for method_decl in [decl for decl in type_decl.body if type(decl) is m.MethodDeclaration]:
        param_strings = []
        for param in method_decl.parameters:
            if type(param.type) is str:
                param_strings.append(param.type + ' ' + param.variable.name)
            else:
                param_strings.append(param.type.name.value + ' ' + param.variable.name)
        print('    ' + method_decl.name + '(' + ', '.join(param_strings) + ')')

        if method_decl.body is not None:
            for statement in method_decl.body:
                # note that this misses variables in inner blocks such as for loops
                # see symbols_visitor.py for a better way of handling this
                if type(statement) is m.VariableDeclaration:
                    for var_decl in statement.variable_declarators:
                        if type(statement.type) is str:
                            type_name = statement.type
                        else:
                            type_name = statement.type.name.value
                        print('        ' + type_name + ' ' + var_decl.variable.name)
