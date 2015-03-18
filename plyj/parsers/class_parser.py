#!/usr/bin/env python2
from plyj.model.annotation import AnnotationMember, \
    AnnotationMethodDeclaration, AnnotationDeclaration, Annotation
from plyj.model.classes import EmptyDeclaration, \
    ConstructorDeclaration, ClassInitializer, FieldDeclaration, \
    ClassDeclaration
from plyj.model.enum import EnumConstant, EnumDeclaration
from plyj.model.interface import InterfaceDeclaration
from plyj.model.method import MethodDeclaration, Throws, FormalParameter
from plyj.model.source_element import collect_tokens, AnonymousSE
from plyj.model.expression import ArrayInitializer


class ClassParser(object):
    @staticmethod
    def p_type_declaration(p):
        """type_declaration : class_declaration
                            | interface_declaration
                            | enum_declaration
                            | annotation_type_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_type_declaration2(p):
        """type_declaration : ';' """
        p[0] = EmptyDeclaration()
        collect_tokens(p)

    @staticmethod
    def p_class_declaration(p):
        """class_declaration : class_header class_body"""
        p[0] = ClassDeclaration(p[1].value['name'], p[2],
                                modifiers=p[1].value['modifiers'],
                                extends=p[1].value['extends'],
                                implements=p[1].value['implements'],
                                type_parameters=p[1].value['type_parameters'])
        # Take tokens out of AnonymousSE of class_header and move
        # them into the new ClassDeclaration.
        p[0].add_tokens_left(p[1])

    @staticmethod
    def p_class_header(p):
        """class_header : class_header_name class_header_extends_opt \
                          class_header_implements_opt"""
        p[1].value['extends'] = p[2]
        p[1].value['implements'] = p[3]
        p[0] = p[1]

    @staticmethod
    def p_class_header_name(p):
        """class_header_name : class_header_name1 type_parameters
                             | class_header_name1"""
        if len(p) == 2:
            p[1].value['type_parameters'] = []
        else:
            p[1].value['type_parameters'] = p[2]
            p[1].add_tokens_right(p[2])
        p[0] = p[1]

    @staticmethod
    def p_class_header_name1(p):
        """class_header_name1 : modifiers_opt CLASS simple_name"""
        p[0] = {'modifiers': p[1], 'name': p[3]}
        collect_tokens(p)

    @staticmethod
    def p_class_header_extends_opt(p):
        """class_header_extends_opt : class_header_extends
                                    | empty"""
        p[0] = p[1]

    @staticmethod
    def p_class_header_extends(p):
        """class_header_extends : EXTENDS class_type"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_class_header_implements_opt(p):
        """class_header_implements_opt : class_header_implements
                                       | empty"""
        p[0] = p[1]

    @staticmethod
    def p_class_header_implements(p):
        """class_header_implements : IMPLEMENTS interface_type_list"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_interface_type_list(p):
        """interface_type_list : interface_type
                               | interface_type_list ',' interface_type"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[3])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_interface_type(p):
        """interface_type : class_or_interface_type"""
        p[0] = p[1]

    @staticmethod
    def p_class_body(p):
        """class_body : '{' class_body_declarations_opt '}' """
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_class_body_declarations_opt(p):
        """class_body_declarations_opt : class_body_declarations"""
        p[0] = p[1]

    @staticmethod
    def p_class_body_declarations_opt2(p):
        """class_body_declarations_opt : empty"""
        p[0] = AnonymousSE([])

    @staticmethod
    def p_class_body_declarations(p):
        """class_body_declarations \
               : class_body_declaration
               | class_body_declarations class_body_declaration"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[2])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_class_body_declaration(p):
        """class_body_declaration : class_member_declaration
                                  | static_initializer
                                  | constructor_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_class_body_declaration2(p):
        """class_body_declaration : block"""
        p[0] = ClassInitializer(p[1])

    @staticmethod
    def p_class_member_declaration(p):
        """class_member_declaration : field_declaration
                                    | class_declaration
                                    | method_declaration
                                    | interface_declaration
                                    | enum_declaration
                                    | annotation_type_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_class_member_declaration2(p):
        """class_member_declaration : ';' """
        p[0] = EmptyDeclaration()
        collect_tokens(p)

    @staticmethod
    def p_field_declaration(p):
        """field_declaration : modifiers_opt type variable_declarators ';' """
        p[0] = FieldDeclaration(p[2], p[3], modifiers=p[1])
        collect_tokens(p)

    @staticmethod
    def p_static_initializer(p):
        """static_initializer : STATIC block"""
        p[0] = ClassInitializer(p[2], static=True)
        collect_tokens(p)

    @staticmethod
    def p_constructor_declaration(p):
        """constructor_declaration : constructor_header method_body"""
        p[1].set_body(p[2])
        p[0] = p[1]

    @staticmethod
    def p_constructor_header(p):
        """constructor_header \
               : constructor_header_name formal_parameter_list_opt ')' \
                 method_header_throws_clause_opt"""
        p[1].set_parameters(p[2])
        p[1].set_throws(p[4])
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_constructor_header_name(p):
        """constructor_header_name \
               : modifiers_opt type_parameters simple_name '('
               | modifiers_opt simple_name '(' """
        if len(p) == 4:
            p[0] = ConstructorDeclaration(p[2],
                                          modifiers=p[1],
                                          type_parameters=[])
        else:
            p[0] = ConstructorDeclaration(p[3],
                                          modifiers=p[1],
                                          type_parameters=p[2])
        collect_tokens(p)

    @staticmethod
    def p_formal_parameter_list_opt(p):
        """formal_parameter_list_opt : formal_parameter_list"""
        p[0] = p[1]

    @staticmethod
    def p_formal_parameter_list_opt2(p):
        """formal_parameter_list_opt : empty"""
        p[0] = AnonymousSE([])

    @staticmethod
    def p_formal_parameter_list(p):
        """formal_parameter_list \
               : formal_parameter
               | formal_parameter_list ',' formal_parameter"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[3])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_formal_parameter(p):
        """formal_parameter \
               : modifiers_opt type variable_declarator_id
               | modifiers_opt type ELLIPSIS variable_declarator_id"""
        if len(p) == 4:
            p[0] = FormalParameter(p[3], p[2], modifiers=p[1])
        else:
            p[0] = FormalParameter(p[4], p[2], modifiers=p[1], vararg=True)
        collect_tokens(p)

    @staticmethod
    def p_method_header_throws_clause_opt(p):
        """method_header_throws_clause_opt : method_header_throws_clause
                                           | empty"""
        p[0] = p[1]

    @staticmethod
    def p_method_header_throws_clause(p):
        """method_header_throws_clause : THROWS class_type_list"""
        p[0] = Throws(p[2])
        collect_tokens(p)

    @staticmethod
    def p_class_type_list(p):
        """class_type_list : class_type_elt
                           | class_type_list ',' class_type_elt"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[3])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_class_type_elt(p):
        """class_type_elt : class_type"""
        p[0] = p[1]

    @staticmethod
    def p_method_body(p):
        """method_body : '{' block_statements_opt '}' """
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_method_declaration(p):
        """method_declaration : abstract_method_declaration
                              | method_header method_body"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p1 = p[1].value
            p[0] = MethodDeclaration(p1['name'],
                                     parameters=p1['parameters'],
                                     extended_dims=p1['extended_dims'],
                                     type_parameters=p1['type_parameters'],
                                     return_type=p1['type'],
                                     modifiers=p1['modifiers'],
                                     throws=p1['throws'],
                                     body=p[2])
            p[0].add_tokens_left(p[1])

    @staticmethod
    def p_abstract_method_declaration(p):
        """abstract_method_declaration : method_header ';' """
        p1 = p[1].value
        p[0] = MethodDeclaration(p1['name'],
                                 abstract=True,
                                 parameters=p1['parameters'],
                                 extended_dims=p1['extended_dims'],
                                 type_parameters=p1['type_parameters'],
                                 return_type=p1['type'],
                                 modifiers=p1['modifiers'],
                                 throws=p1['throws'])
        p[0].add_tokens_left(p[1])
        collect_tokens(p)

    @staticmethod
    def p_method_header(p):
        """method_header \
               : method_header_name formal_parameter_list_opt ')' \
                 method_header_extended_dims method_header_throws_clause_opt"""
        p[1].value['parameters'] = p[2]
        p[1].value['extended_dims'] = p[4]
        p[1].value['throws'] = p[5]
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_method_header_name(p):
        """method_header_name \
               : modifiers_opt type_parameters type simple_name '('
               | modifiers_opt type simple_name '(' """
        if len(p) == 5:
            p[0] = {
                'modifiers': p[1],
                'type_parameters': [],
                'type': p[2],
                'name': p[3]
            }
        else:
            p[0] = {
                'modifiers': p[1],
                'type_parameters': p[2],
                'type': p[3],
                'name': p[4]
            }
        collect_tokens(p)

    @staticmethod
    def p_method_header_extended_dims(p):
        """method_header_extended_dims : dims_opt"""
        p[0] = p[1]

    @staticmethod
    def p_interface_declaration(p):
        """interface_declaration : interface_header interface_body"""
        header = p[1].value
        p[0] = InterfaceDeclaration(header['name'],
                                    modifiers=header['modifiers'],
                                    type_parameters=header['type_parameters'],
                                    extends=header['extends'],
                                    body=p[2])
        p[0].add_tokens_left(p[1])

    @staticmethod
    def p_interface_header(p):
        """interface_header \
               : interface_header_name interface_header_extends_opt"""
        p[1].value['extends'] = p[2]
        p[0] = p[1]

    @staticmethod
    def p_interface_header_name(p):
        """interface_header_name : interface_header_name1 type_parameters
                                 | interface_header_name1"""
        if len(p) == 2:
            p[1].value['type_parameters'] = []
        else:
            p[1].value['type_parameters'] = p[2]
        p[0] = p[1]

    @staticmethod
    def p_interface_header_name1(p):
        """interface_header_name1 \
               : modifiers_opt INTERFACE simple_name"""
        p[0] = {'modifiers': p[1], 'name': p[3]}
        collect_tokens(p)

    @staticmethod
    def p_interface_header_extends_opt(p):
        """interface_header_extends_opt : interface_header_extends"""
        p[0] = p[1]

    @staticmethod
    def p_interface_header_extends_opt2(p):
        """interface_header_extends_opt : empty"""
        p[0] = AnonymousSE([])

    @staticmethod
    def p_interface_header_extends(p):
        """interface_header_extends : EXTENDS interface_type_list"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_interface_body(p):
        """interface_body : '{' interface_member_declarations_opt '}' """
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_interface_member_declarations_opt(p):
        """interface_member_declarations_opt : interface_member_declarations"""
        p[0] = p[1]

    @staticmethod
    def p_interface_member_declarations_opt2(p):
        """interface_member_declarations_opt : empty"""
        p[0] = []

    @staticmethod
    def p_interface_member_declarations(p):
        """interface_member_declarations \
               : interface_member_declaration
               | interface_member_declarations interface_member_declaration"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_interface_member_declaration(p):
        """interface_member_declaration : constant_declaration
                                        | abstract_method_declaration
                                        | class_declaration
                                        | interface_declaration
                                        | enum_declaration
                                        | annotation_type_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_interface_member_declaration2(p):
        """interface_member_declaration : ';' """
        p[0] = EmptyDeclaration()
        collect_tokens(p)

    @staticmethod
    def p_constant_declaration(p):
        """constant_declaration : field_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_enum_declaration(p):
        """enum_declaration : enum_header enum_body"""
        p[0] = EnumDeclaration(p[1].value['name'],
                               implements=p[1].value['implements'],
                               modifiers=p[1].value['modifiers'],
                               type_parameters=p[1].value['type_parameters'],
                               body=p[2])

    @staticmethod
    def p_enum_header(p):
        """enum_header : enum_header_name class_header_implements_opt"""
        if p[2] is not None:
            p[1].value['implements'] = p[2].value
            p[1].add_tokens_right(p[2])
        else:
            p[1].value['implements'] = []
        p[0] = p[1]

    @staticmethod
    def p_enum_header_name(p):
        """enum_header_name \
               : modifiers_opt ENUM simple_name
               | modifiers_opt ENUM simple_name type_parameters"""
        if len(p) == 4:
            p[0] = {'modifiers': p[1], 'name': p[3], 'type_parameters': []}
        else:
            p[0] = {'modifiers': p[1], 'name': p[3], 'type_parameters': p[4]}
        collect_tokens(p)

    @staticmethod
    def p_enum_body(p):
        """enum_body : '{' enum_body_declarations_opt '}' """
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_enum_body2(p):
        """enum_body : '{' ',' enum_body_declarations_opt '}' """
        p[0] = p[3]
        collect_tokens(p)

    @staticmethod
    def p_enum_body3(p):
        """enum_body : '{' enum_constants ',' enum_body_declarations_opt '}'
        """
        p[2].value.extend(p[4].value)
        p[2].add_tokens_right(p[4])
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_enum_body4(p):
        """enum_body : '{' enum_constants enum_body_declarations_opt '}' """
        if p[3] is None:
            p[0] = p[2]
        else:
            p[2].value.extend(p[3].value)
            p[2].add_tokens_right(p[3])
            p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_enum_constants(p):
        """enum_constants : enum_constant
                          | enum_constants ',' enum_constant"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[3])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_enum_constant(p):
        """enum_constant : enum_constant_header class_body
                         | enum_constant_header"""
        p1 = p[1].value
        if len(p) == 2:
            p[0] = EnumConstant(p1['name'],
                                arguments=p1['arguments'],
                                modifiers=p1['modifiers'])
        else:
            p[0] = EnumConstant(p1['name'],
                                arguments=p1['arguments'],
                                modifiers=p1['modifiers'],
                                body=p[2])
        p[0].add_tokens_left(p[1])

    @staticmethod
    def p_enum_constant_header(p):
        """enum_constant_header : enum_constant_header_name arguments_opt"""
        p[1].value['arguments'] = p[2]
        p[0] = p[1]

    @staticmethod
    def p_enum_constant_header_name(p):
        """enum_constant_header_name : modifiers_opt simple_name"""
        p[0] = {'modifiers': p[1], 'name': p[2]}
        collect_tokens(p)

    @staticmethod
    def p_arguments_opt(p):
        """arguments_opt : arguments"""
        p[0] = p[1]

    @staticmethod
    def p_arguments_opt2(p):
        """arguments_opt : empty"""
        p[0] = AnonymousSE([])

    @staticmethod
    def p_arguments(p):
        """arguments : '(' argument_list_opt ')' """
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_argument_list_opt(p):
        """argument_list_opt : argument_list"""
        p[0] = p[1]

    @staticmethod
    def p_argument_list_opt2(p):
        """argument_list_opt : empty"""
        p[0] = AnonymousSE([])

    @staticmethod
    def p_argument_list(p):
        """argument_list : expression
                         | argument_list ',' expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[3])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_enum_body_declarations_opt(p):
        """enum_body_declarations_opt : enum_declarations"""
        p[0] = p[1]

    @staticmethod
    def p_enum_body_declarations_opt2(p):
        """enum_body_declarations_opt : empty"""
        p[0] = AnonymousSE([])

    @staticmethod
    def p_enum_body_declarations(p):
        """enum_declarations : ';' class_body_declarations_opt"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_annotation_type_declaration(p):
        """annotation_type_declaration \
               : annotation_type_declaration_header annotation_type_body"""
        p1 = p[1].value
        p[0] = AnnotationDeclaration(p1['name'],
                                     modifiers=p1['modifiers'],
                                     type_parameters=p1['type_parameters'],
                                     extends=p1['extends'],
                                     implements=p1['implements'],
                                     body=p[2])
        p[0].add_tokens_left(p[1])

    @staticmethod
    def p_annotation_type_declaration_header(p):
        """annotation_type_declaration_header \
               : annotation_type_declaration_header_name \
                 class_header_extends_opt class_header_implements_opt"""
        if p[2] is not None:
            p[1].value['extends'] = p[2]
        if p[3] is not None:
            p[1].value['implements'] = p[3].value
            p[1].add_tokens_right(p[3])
        p[0] = p[1]

    @staticmethod
    def p_annotation_type_declaration_header_name(p):
        """annotation_type_declaration_header_name \
               : modifiers '@' INTERFACE simple_name"""
        p[0] = {'modifiers': p[1], 'name': p[4], 'type_parameters': [],
                'extends': None, 'implements': None}
        collect_tokens(p)

    @staticmethod
    def p_annotation_type_declaration_header_name2(p):
        """annotation_type_declaration_header_name \
               : modifiers '@' INTERFACE simple_name \
                 type_parameters"""
        p[0] = {'modifiers': p[1], 'name': p[4], 'type_parameters': p[5],
                'extends': None, 'implements': None}
        collect_tokens(p)

    @staticmethod
    def p_annotation_type_declaration_header_name3(p):
        """annotation_type_declaration_header_name \
               : '@' INTERFACE simple_name type_parameters"""
        p[0] = {'modifiers': [], 'name': p[3], 'type_parameters': p[4],
                'extends': None, 'implements': None}
        collect_tokens(p)

    @staticmethod
    def p_annotation_type_declaration_header_name4(p):
        """annotation_type_declaration_header_name \
               : '@' INTERFACE simple_name"""
        p[0] = {'modifiers': [], 'name': p[3], 'type_parameters': [],
                'extends': None, 'implements': None}
        collect_tokens(p)

    @staticmethod
    def p_annotation_type_body(p):
        """annotation_type_body \
               : '{' annotation_type_member_declarations_opt '}' """
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_annotation_type_member_declarations_opt(p):
        """annotation_type_member_declarations_opt \
               : annotation_type_member_declarations"""
        p[0] = p[1]

    @staticmethod
    def p_annotation_type_member_declarations_opt2(p):
        """annotation_type_member_declarations_opt : empty"""
        p[0] = []

    @staticmethod
    def p_annotation_type_member_declarations(p):
        """annotation_type_member_declarations \
               : annotation_type_member_declaration
               | annotation_type_member_declarations \
                 annotation_type_member_declaration"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_annotation_type_member_declaration(p):
        """annotation_type_member_declaration : annotation_method_header ';'
                                              | constant_declaration
                                              | constructor_declaration
                                              | type_declaration"""
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_annotation_method_header(p):
        """annotation_method_header \
               : annotation_method_header_name formal_parameter_list_opt ')' \
                 method_header_extended_dims \
                 annotation_method_header_default_value_opt"""
        p[0] = AnnotationMethodDeclaration(
            p[1].value['name'], p[1].value['type'], parameters=p[2],
            default=p[5], extended_dims=p[4],
            type_parameters=p[1].value['type_parameters'],
            modifiers=p[1].value['modifiers'])
        p[0].add_tokens_right(p[1])
        collect_tokens(p)

    @staticmethod
    def p_annotation_method_header_name(p):
        """annotation_method_header_name \
               : modifiers_opt type_parameters type simple_name '('
               | modifiers_opt type simple_name '(' """
        if len(p) == 5:
            p[0] = {
                'modifiers': p[1],
                'type_parameters': [],
                'type': p[2],
                'name': p[3]
            }
        else:
            p[0] = {
                'modifiers': p[1],
                'type_parameters': p[2],
                'type': p[3],
                'name': p[4]
            }
        collect_tokens(p)

    @staticmethod
    def p_annotation_method_header_default_value_opt(p):
        """annotation_method_header_default_value_opt : default_value
                                                      | empty"""
        p[0] = p[1]

    @staticmethod
    def p_default_value(p):
        """default_value : DEFAULT member_value"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_member_value(p):
        """member_value : conditional_expression_not_name
                        | name
                        | annotation
                        | member_value_array_initializer"""
        p[0] = p[1]

    @staticmethod
    def p_member_value_array_initializer(p):
        """member_value_array_initializer : '{' member_values ',' '}'
                                          | '{' member_values '}' """
        p[0] = ArrayInitializer(p[2])
        collect_tokens(p)

    @staticmethod
    def p_member_value_array_initializer2(p):
        """member_value_array_initializer : '{' ',' '}'
                                          | '{' '}' """
        p[0] = ArrayInitializer()
        collect_tokens(p)

    @staticmethod
    def p_member_values(p):
        """member_values : member_value
                         | member_values ',' member_value"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[3])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_annotation(p):
        """annotation : normal_annotation
                      | marker_annotation
                      | single_member_annotation"""
        p[0] = p[1]

    @staticmethod
    def p_normal_annotation(p):
        """normal_annotation \
               : annotation_name '(' member_value_pairs_opt ')' """
        p[0] = Annotation(p[1], members=p[3])
        collect_tokens(p)

    @staticmethod
    def p_annotation_name(p):
        """annotation_name : '@' name"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_member_value_pairs_opt(p):
        """member_value_pairs_opt : member_value_pairs"""
        p[0] = p[1]

    @staticmethod
    def p_member_value_pairs_opt2(p):
        """member_value_pairs_opt : empty"""
        p[0] = AnonymousSE([])

    @staticmethod
    def p_member_value_pairs(p):
        """member_value_pairs : member_value_pair
                              | member_value_pairs ',' member_value_pair"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].value.append(p[3])
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_member_value_pair(p):
        """member_value_pair : simple_name '=' member_value"""
        p[0] = AnnotationMember(p[1], p[3])
        collect_tokens(p)

    @staticmethod
    def p_marker_annotation(p):
        """marker_annotation : annotation_name"""
        p[0] = Annotation(p[1])

    @staticmethod
    def p_single_member_annotation(p):
        """single_member_annotation \
               : annotation_name '(' single_member_annotation_member_value ')'
        """
        p[0] = Annotation(p[1], single_member=p[3])
        collect_tokens(p)

    @staticmethod
    def p_single_member_annotation_member_value(p):
        """single_member_annotation_member_value : member_value"""
        p[0] = p[1]