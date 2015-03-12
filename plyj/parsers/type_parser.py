#!/usr/bin/env python2
from plyj.model.classes import WildcardBound, Wildcard
from plyj.model.name import PrimitiveType
from plyj.model.source_element import collect_tokens
from plyj.model.type import Type, TypeParameter


class TypeParser(object):
    @staticmethod
    def p_modifiers_opt(p):
        """modifiers_opt : modifiers"""
        p[0] = p[1]

    @staticmethod
    def p_modifiers_opt2(p):
        """modifiers_opt : empty"""
        p[0] = []

    @staticmethod
    def p_modifiers(p):
        """modifiers : modifier
                     | modifiers modifier"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_modifier(p):
        """modifier : PUBLIC
                    | PROTECTED
                    | PRIVATE
                    | STATIC
                    | ABSTRACT
                    | FINAL
                    | NATIVE
                    | SYNCHRONIZED
                    | TRANSIENT
                    | VOLATILE
                    | STRICTFP"""
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_modifier2(p):
        """modifier : annotation"""
        p[0] = p[1]

    @staticmethod
    def p_type(p):
        """type : primitive_type
                | reference_type"""
        p[0] = p[1]

    @staticmethod
    def p_primitive_type(p):
        """primitive_type : BOOLEAN
                          | VOID
                          | BYTE
                          | SHORT
                          | INT
                          | LONG
                          | CHAR
                          | FLOAT
                          | DOUBLE"""
        p[0] = PrimitiveType(p[1])
        collect_tokens(p)

    @staticmethod
    def p_reference_type(p):
        """reference_type : class_or_interface_type
                          | array_type"""
        p[0] = p[1]

    @staticmethod
    def p_class_or_interface_type(p):
        """class_or_interface_type : class_or_interface
                                   | generic_type"""
        p[0] = p[1]

    @staticmethod
    def p_class_type(p):
        """class_type : class_or_interface_type"""
        p[0] = p[1]

    @staticmethod
    def p_class_or_interface(p):
        """class_or_interface : name
                              | generic_type '.' name"""
        if len(p) == 2:
            p[0] = Type(p[1])
        else:
            p[0] = Type(p[3], enclosed_in=p[1])
        collect_tokens(p)

    @staticmethod
    def p_generic_type(p):
        """generic_type : class_or_interface type_arguments"""
        p[1].type_arguments = p[2]
        p[0] = p[1]

    @staticmethod
    def p_generic_type2(p):
        """generic_type : class_or_interface '<' '>' """
        p[0] = Type(p[1], type_arguments='diamond')
        collect_tokens(p)

    @staticmethod
    def p_array_type(p):
        """array_type : primitive_type dims
                      | name dims"""
        p[0] = Type(p[1], dimensions=p[2])

    @staticmethod
    def p_array_type2(p):
        """array_type : generic_type dims"""
        p[1].dims = p[2]
        p[0] = p[1]

    @staticmethod
    def p_array_type3(p):
        """array_type : generic_type '.' name dims"""
        p[0] = Type(p[3], enclosed_in=p[1], dimensions=p[4])
        collect_tokens(p)

    @staticmethod
    def p_type_arguments(p):
        """type_arguments : '<' type_argument_list1"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_type_argument_list1(p):
        """type_argument_list1 : type_argument1
                               | type_argument_list ',' type_argument1"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        collect_tokens(p)

    @staticmethod
    def p_type_argument_list(p):
        """type_argument_list : type_argument
                              | type_argument_list ',' type_argument"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        collect_tokens(p)

    @staticmethod
    def p_type_argument(p):
        """type_argument : reference_type
                         | wildcard"""
        p[0] = p[1]

    @staticmethod
    def p_type_argument1(p):
        """type_argument1 : reference_type1
                          | wildcard1"""
        p[0] = p[1]

    @staticmethod
    def p_reference_type1(p):
        """reference_type1 : reference_type '>'
                           | class_or_interface '<' type_argument_list2"""
        if len(p) == 3:
            p[0] = p[1]
        else:
            p[1].type_arguments = p[3]
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_type_argument_list2(p):
        """type_argument_list2 : type_argument2
                               | type_argument_list ',' type_argument2"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        collect_tokens(p)

    @staticmethod
    def p_type_argument2(p):
        """type_argument2 : reference_type2
                          | wildcard2"""
        p[0] = p[1]

    @staticmethod
    def p_reference_type2(p):
        """reference_type2 : reference_type RSHIFT
                           | class_or_interface '<' type_argument_list3"""
        if len(p) == 3:
            p[0] = p[1]
        else:
            p[1].type_arguments = p[3]
            p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_type_argument_list3(p):
        """type_argument_list3 : type_argument3
                               | type_argument_list ',' type_argument3"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        collect_tokens(p)

    @staticmethod
    def p_type_argument3(p):
        """type_argument3 : reference_type3
                          | wildcard3"""
        p[0] = p[1]

    @staticmethod
    def p_reference_type3(p):
        """reference_type3 : reference_type RRSHIFT"""
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_wildcard(p):
        """wildcard : '?'
                    | '?' wildcard_bounds"""
        if len(p) == 2:
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])
        collect_tokens(p)

    @staticmethod
    def p_wildcard_bounds(p):
        """wildcard_bounds : EXTENDS reference_type
                           | SUPER reference_type"""
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)
        collect_tokens(p)

    @staticmethod
    def p_wildcard1(p):
        """wildcard1 : '?' '>'
                     | '?' wildcard_bounds1"""
        if p[2] == '>':
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])
        collect_tokens(p)

    @staticmethod
    def p_wildcard_bounds1(p):
        """wildcard_bounds1 : EXTENDS reference_type1
                            | SUPER reference_type1"""
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)
        collect_tokens(p)

    @staticmethod
    def p_wildcard2(p):
        """wildcard2 : '?' RSHIFT
                     | '?' wildcard_bounds2"""
        if p[2] == '>>':
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])
        collect_tokens(p)

    @staticmethod
    def p_wildcard_bounds2(p):
        """wildcard_bounds2 : EXTENDS reference_type2
                            | SUPER reference_type2"""
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)
        collect_tokens(p)

    @staticmethod
    def p_wildcard3(p):
        """wildcard3 : '?' RRSHIFT
                     | '?' wildcard_bounds3"""
        if p[2] == '>>>':
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])
        collect_tokens(p)

    @staticmethod
    def p_wildcard_bounds3(p):
        """wildcard_bounds3 : EXTENDS reference_type3
                            | SUPER reference_type3"""
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)
        collect_tokens(p)

    @staticmethod
    def p_type_parameter_header(p):
        """type_parameter_header : strictly_simple_name"""
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_type_parameters(p):
        """type_parameters : '<' type_parameter_list1"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_type_parameter_list(p):
        """type_parameter_list : type_parameter
                               | type_parameter_list ',' type_parameter"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        collect_tokens(p)

    @staticmethod
    def p_type_parameter(p):
        """type_parameter \
               : type_parameter_header
               | type_parameter_header EXTENDS reference_type
               | type_parameter_header EXTENDS reference_type \
                 additional_bound_list"""
        if len(p) == 2:
            p[0] = TypeParameter(p[1])
        elif len(p) == 4:
            p[0] = TypeParameter(p[1], extends=[p[3]])
        else:
            p[0] = TypeParameter(p[1], extends=[p[3]] + p[4])
        collect_tokens(p)

    @staticmethod
    def p_additional_bound_list(p):
        """additional_bound_list : additional_bound
                                 | additional_bound_list additional_bound"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_additional_bound(p):
        """additional_bound : '&' reference_type"""
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_type_parameter_list1(p):
        """type_parameter_list1 : type_parameter1
                                | type_parameter_list ',' type_parameter1"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        collect_tokens(p)

    @staticmethod
    def p_type_parameter1(p):
        """type_parameter1 \
               : type_parameter_header '>'
               | type_parameter_header EXTENDS reference_type1
               | type_parameter_header EXTENDS reference_type \
                 additional_bound_list1"""
        if len(p) == 3:
            p[0] = TypeParameter(p[1])
        elif len(p) == 4:
            p[0] = TypeParameter(p[1], extends=[p[3]])
        else:
            p[0] = TypeParameter(p[1], extends=[p[3]] + p[4])
        collect_tokens(p)

    @staticmethod
    def p_additional_bound_list1(p):
        """additional_bound_list1 : additional_bound1
                                  | additional_bound_list additional_bound1"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_additional_bound1(p):
        """additional_bound1 : '&' reference_type1"""
        p[0] = p[2]
        collect_tokens(p)