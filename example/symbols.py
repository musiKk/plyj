#!/usr/bin/env python2

import sys
from plyj.model.classes import FieldDeclaration
from plyj.model.method import MethodDeclaration
from plyj.model.statement import VariableDeclaration
from plyj.parser import Parser

p = Parser()
tree = p.parse_file(sys.argv[1])

print('declared types:')
for type_decl in tree.type_declarations:
    print(type_decl.name.serialize())
    if type_decl.extends is not None:
        print(' -> extending ' + type_decl.extends.name.serialize())
    if len(type_decl.implements) != 0:
        implements = (type_.serialize() for type_ in type_decl.implements)
        print(' -> implementing ' + ', '.join(implements))

    print('fields:')
    for field_decl in type_decl.body:
        if not isinstance(field_decl, FieldDeclaration):
            continue
        print('    ' + field_decl.serialize())

    print('methods:')
    for method_decl in type_decl.body:
        if not isinstance(method_decl, MethodDeclaration):
            continue

        param_strings = (param.serialize() for param in method_decl.parameters)
        name = method_decl.name.serialize()
        print('    ' + name + '(' + ', '.join(param_strings) + ')')

        if method_decl.body is not None:
            for statement in method_decl.body:
                # note that this misses variables in inner blocks such as for
                # loops see symbols_visitor.py for a better way of handling
                # this
                if type(statement) is VariableDeclaration:
                    print('        ' + statement.serialize())