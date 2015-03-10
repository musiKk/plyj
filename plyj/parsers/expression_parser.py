#!/usr/bin/env python2
from plyj.model.expression import Assignment, Cast, Unary, Multiplicative, \
    Additive, Shift, Relational, InstanceOf, Equality, ConditionalAnd, \
    ConditionalOr, Conditional, Or, Xor, And
from plyj.model.literal import ClassLiteral
from plyj.model.source_element import collect_tokens, ensure_se, AnonymousSourceElement
from plyj.model.type import Type


class ExpressionParser(object):
    @staticmethod
    def p_expression(p):
        """expression : assignment_expression"""
        p[0] = p[1]

    @staticmethod
    def p_expression_not_name(p):
        """expression_not_name : assignment_expression_not_name"""
        p[0] = p[1]

    @staticmethod
    def p_assignment_expression(p):
        """assignment_expression : assignment
                                 | conditional_expression"""
        p[0] = p[1]

    @staticmethod
    def p_assignment_expression_not_name(p):
        """assignment_expression_not_name : assignment
                                          | conditional_expression_not_name"""
        p[0] = p[1]

    @staticmethod
    def p_assignment(p):
        """assignment : postfix_expression assignment_operator \
                        assignment_expression"""
        p[0] = Assignment(p[2], p[1], p[3])

    @staticmethod
    def p_assignment_operator(p):
        """assignment_operator : '='
                               | TIMES_ASSIGN
                               | DIVIDE_ASSIGN
                               | REMAINDER_ASSIGN
                               | PLUS_ASSIGN
                               | MINUS_ASSIGN
                               | LSHIFT_ASSIGN
                               | RSHIFT_ASSIGN
                               | RRSHIFT_ASSIGN
                               | AND_ASSIGN
                               | OR_ASSIGN
                               | XOR_ASSIGN"""
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_conditional_expression(p):
        """conditional_expression \
               : conditional_or_expression
               | conditional_or_expression \
                 '?' expression \
                 ':' conditional_expression"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1], p[3], p[5])
        collect_tokens(p)

    @staticmethod
    def p_conditional_expression_not_name(p):
        """conditional_expression_not_name \
               : conditional_or_expression_not_name
               | conditional_or_expression_not_name \
                 '?' expression \
                 ':' conditional_expression
               | name '?' expression ':' conditional_expression"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1], p[3], p[5])
        collect_tokens(p)

    @staticmethod
    def binary_operator(p, ctor):
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ctor(p[2], p[1], p[3])
        collect_tokens(p)

    @staticmethod
    def p_conditional_or_expression(p):
        """conditional_or_expression \
               : conditional_and_expression
               | conditional_or_expression OR conditional_and_expression"""
        ExpressionParser.binary_operator(p, ConditionalOr)

    @staticmethod
    def p_conditional_or_expression_not_name(p):
        """conditional_or_expression_not_name \
               : conditional_and_expression_not_name
               | conditional_or_expression_not_name \
                 OR conditional_and_expression
               | name OR conditional_and_expression"""
        ExpressionParser.binary_operator(p, ConditionalOr)

    @staticmethod
    def p_conditional_and_expression(p):
        """conditional_and_expression \
               : inclusive_or_expression
               | conditional_and_expression AND inclusive_or_expression"""
        ExpressionParser.binary_operator(p, ConditionalAnd)

    @staticmethod
    def p_conditional_and_expression_not_name(p):
        """conditional_and_expression_not_name \
               : inclusive_or_expression_not_name
               | conditional_and_expression_not_name \
                 AND inclusive_or_expression
               | name AND inclusive_or_expression"""
        ExpressionParser.binary_operator(p, ConditionalAnd)

    @staticmethod
    def p_inclusive_or_expression(p):
        """inclusive_or_expression \
               : exclusive_or_expression
               | inclusive_or_expression '|' exclusive_or_expression"""
        ExpressionParser.binary_operator(p, Or)

    @staticmethod
    def p_inclusive_or_expression_not_name(p):
        """inclusive_or_expression_not_name \
               : exclusive_or_expression_not_name
               | inclusive_or_expression_not_name '|' exclusive_or_expression
               | name '|' exclusive_or_expression
        """
        ExpressionParser.binary_operator(p, Or)

    @staticmethod
    def p_exclusive_or_expression(p):
        """exclusive_or_expression : and_expression
                                   | exclusive_or_expression '^' and_expression
        """
        ExpressionParser.binary_operator(p, Xor)

    @staticmethod
    def p_exclusive_or_expression_not_name(p):
        """exclusive_or_expression_not_name \
               : and_expression_not_name
               | exclusive_or_expression_not_name '^' and_expression
               | name '^' and_expression"""
        ExpressionParser.binary_operator(p, Xor)

    @staticmethod
    def p_and_expression(p):
        """and_expression : equality_expression
                          | and_expression '&' equality_expression"""
        ExpressionParser.binary_operator(p, And)

    @staticmethod
    def p_and_expression_not_name(p):
        """and_expression_not_name \
               : equality_expression_not_name
               | and_expression_not_name '&' equality_expression
               | name '&' equality_expression"""
        ExpressionParser.binary_operator(p, And)

    @staticmethod
    def p_equality_expression(p):
        """equality_expression \
               : instanceof_expression
               | equality_expression EQ instanceof_expression
               | equality_expression NEQ instanceof_expression"""
        ExpressionParser.binary_operator(p, Equality)

    @staticmethod
    def p_equality_expression_not_name(p):
        """equality_expression_not_name \
               : instanceof_expression_not_name
               | equality_expression_not_name EQ instanceof_expression
               | name EQ instanceof_expression
               | equality_expression_not_name NEQ instanceof_expression
               | name NEQ instanceof_expression"""
        ExpressionParser.binary_operator(p, Equality)

    @staticmethod
    def p_instanceof_expression(p):
        """instanceof_expression \
               : relational_expression
               | instanceof_expression INSTANCEOF reference_type"""
        ExpressionParser.binary_operator(p, InstanceOf)

    @staticmethod
    def p_instanceof_expression_not_name(p):
        """instanceof_expression_not_name \
               : relational_expression_not_name
               | name INSTANCEOF reference_type
               | instanceof_expression_not_name INSTANCEOF reference_type"""
        ExpressionParser.binary_operator(p, InstanceOf)

    @staticmethod
    def p_relational_expression(p):
        """relational_expression : shift_expression
                                 | relational_expression '>' shift_expression
                                 | relational_expression '<' shift_expression
                                 | relational_expression GTEQ shift_expression
                                 | relational_expression LTEQ shift_expression
        """
        ExpressionParser.binary_operator(p, Relational)

    @staticmethod
    def p_relational_expression_not_name(p):
        """relational_expression_not_name \
               : shift_expression_not_name
               | shift_expression_not_name '<' shift_expression
               | name '<' shift_expression
               | shift_expression_not_name '>' shift_expression
               | name '>' shift_expression
               | shift_expression_not_name GTEQ shift_expression
               | name GTEQ shift_expression
               | shift_expression_not_name LTEQ shift_expression
               | name LTEQ shift_expression"""
        ExpressionParser.binary_operator(p, Relational)

    @staticmethod
    def p_shift_expression(p):
        """shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression
                            | shift_expression RRSHIFT additive_expression"""
        ExpressionParser.binary_operator(p, Shift)

    @staticmethod
    def p_shift_expression_not_name(p):
        """shift_expression_not_name \
               : additive_expression_not_name
               | shift_expression_not_name LSHIFT additive_expression
               | name LSHIFT additive_expression
               | shift_expression_not_name RSHIFT additive_expression
               | name RSHIFT additive_expression
               | shift_expression_not_name RRSHIFT additive_expression
               | name RRSHIFT additive_expression"""
        ExpressionParser.binary_operator(p, Shift)

    @staticmethod
    def p_additive_expression(p):
        """additive_expression \
               : multiplicative_expression
               | additive_expression '+' multiplicative_expression
               | additive_expression '-' multiplicative_expression"""
        ExpressionParser.binary_operator(p, Additive)

    @staticmethod
    def p_additive_expression_not_name(p):
        """additive_expression_not_name \
               : multiplicative_expression_not_name
               | additive_expression_not_name '+' multiplicative_expression
               | name '+' multiplicative_expression
               | additive_expression_not_name '-' multiplicative_expression
               | name '-' multiplicative_expression"""
        ExpressionParser.binary_operator(p, Additive)

    @staticmethod
    def p_multiplicative_expression(p):
        """multiplicative_expression \
               : unary_expression
               | multiplicative_expression '*' unary_expression
               | multiplicative_expression '/' unary_expression
               | multiplicative_expression '%' unary_expression"""
        ExpressionParser.binary_operator(p, Multiplicative)

    @staticmethod
    def p_multiplicative_expression_not_name(p):
        """multiplicative_expression_not_name \
               : unary_expression_not_name
               | multiplicative_expression_not_name '*' unary_expression
               | name '*' unary_expression
               | multiplicative_expression_not_name '/' unary_expression
               | name '/' unary_expression
               | multiplicative_expression_not_name '%' unary_expression
               | name '%' unary_expression"""
        ExpressionParser.binary_operator(p, Multiplicative)

    @staticmethod
    def p_unary_expression(p):
        """unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | '+' unary_expression
                            | '-' unary_expression
                            | unary_expression_not_plus_minus"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])
        collect_tokens(p)

    @staticmethod
    def p_unary_expression_not_name(p):
        """unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | '+' unary_expression
                                     | '-' unary_expression
                                     | unary_expression_not_plus_minus_not_name
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])
        collect_tokens(p)

    @staticmethod
    def p_pre_increment_expression(p):
        """pre_increment_expression : PLUSPLUS unary_expression"""
        p[0] = Unary('++x', p[2])
        collect_tokens(p)

    @staticmethod
    def p_pre_decrement_expression(p):
        """pre_decrement_expression : MINUSMINUS unary_expression"""
        p[0] = Unary('--x', p[2])
        collect_tokens(p)

    @staticmethod
    def p_unary_expression_not_plus_minus(p):
        """unary_expression_not_plus_minus : postfix_expression
                                           | '~' unary_expression
                                           | '!' unary_expression
                                           | cast_expression"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])
        collect_tokens(p)

    @staticmethod
    def p_unary_expression_not_plus_minus_not_name(p):
        """unary_expression_not_plus_minus_not_name \
               : postfix_expression_not_name
               | '~' unary_expression
               | '!' unary_expression
               | cast_expression"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])
        collect_tokens(p)

    @staticmethod
    def p_postfix_expression(p):
        """postfix_expression : primary
                              | name
                              | post_increment_expression
                              | post_decrement_expression"""
        p[0] = p[1]

    @staticmethod
    def p_postfix_expression_not_name(p):
        """postfix_expression_not_name : primary
                                       | post_increment_expression
                                       | post_decrement_expression"""
        p[0] = p[1]

    @staticmethod
    def p_post_increment_expression(p):
        """post_increment_expression : postfix_expression PLUSPLUS"""
        p[0] = Unary('x++', p[1])
        collect_tokens(p)

    @staticmethod
    def p_post_decrement_expression(p):
        """post_decrement_expression : postfix_expression MINUSMINUS"""
        p[0] = Unary('x--', p[1])
        collect_tokens(p)

    @staticmethod
    def p_primary(p):
        """primary : primary_no_new_array
                   | array_creation_with_array_initializer
                   | array_creation_without_array_initializer"""
        p[0] = p[1]

    @staticmethod
    def p_primary_no_new_array(p):
        """primary_no_new_array : literal
                                | THIS
                                | class_instance_creation_expression
                                | field_access
                                | method_invocation
                                | array_access"""
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_primary_no_new_array2(p):
        """primary_no_new_array : '(' name ')'
                                | '(' expression_not_name ')' """
        p[0] = p[2]
        collect_tokens(p)

    @staticmethod
    def p_primary_no_new_array3(p):
        """primary_no_new_array : name '.' THIS
                                | name '.' SUPER"""
        p[1].append_name(p[3])
        p[0] = p[1]
        collect_tokens(p)

    @staticmethod
    def p_primary_no_new_array4(p):
        """primary_no_new_array : name '.' CLASS
                                | name dims '.' CLASS
                                | primitive_type dims '.' CLASS
                                | primitive_type '.' CLASS"""
        if len(p) == 4:
            p[0] = ClassLiteral(Type(p[1]))
        else:
            p[0] = ClassLiteral(Type(p[1], dimensions=p[2]))
        collect_tokens(p)

    @staticmethod
    def p_dims_opt(p):
        """dims_opt : dims"""
        p[0] = p[1]

    @staticmethod
    def p_dims_opt2(p):
        """dims_opt : empty"""
        p[0] = 0

    @staticmethod
    def p_dims(p):
        """dims : dims_loop"""
        p[0] = p[1]

    @staticmethod
    def p_dims_loop(p):
        """dims_loop : one_dim_loop
                     | dims_loop one_dim_loop"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[1].add_tokens_right(p[2])
            p[1].value += p[2].value
            p[0] = p[1]

    @staticmethod
    def p_one_dim_loop(p):
        """one_dim_loop : '[' ']' """
        p[0] = AnonymousSourceElement(1)
        collect_tokens(p)

    @staticmethod
    def p_cast_expression(p):
        """cast_expression : '(' primitive_type dims_opt ')' unary_expression
        """
        p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])
        collect_tokens(p)

    @staticmethod
    def p_cast_expression2(p):
        """cast_expression \
               : '(' name type_arguments dims_opt ')' \
                 unary_expression_not_plus_minus"""
        p[0] = Cast(Type(p[2], type_arguments=p[3], dimensions=p[4]), p[6])
        collect_tokens(p)

    @staticmethod
    def p_cast_expression3(p):
        """cast_expression \
               : '(' name type_arguments \
                 '.' class_or_interface_type dims_opt \
                 ')' unary_expression_not_plus_minus"""
        p[5].dimensions = ensure_se(p[6])
        p[5].enclosed_in = Type(p[2], type_arguments=p[3])
        p[0] = Cast(p[5], p[8])
        collect_tokens(p)

    @staticmethod
    def p_cast_expression4(p):
        """cast_expression : '(' name ')' unary_expression_not_plus_minus"""
        # technically it's not necessarily a type but could be a type parameter
        p[0] = Cast(Type(p[2]), p[4])
        collect_tokens(p)

    @staticmethod
    def p_cast_expression5(p):
        """cast_expression : '(' name dims ')' unary_expression_not_plus_minus
        """
        # technically it's not necessarily a type but could be a type parameter
        p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])
        collect_tokens(p)