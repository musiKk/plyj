#!/usr/bin/env python2
from plyj.model import Block, ArrayCreation, ArrayAccess, FieldAccess, \
    InstanceCreation, ConstructorInvocation, Try, Catch, Throw, DoWhile, \
    SwitchCase, Switch, ForEach, IfThenElse, MethodInvocation, \
    ArrayInitializer, ExpressionStatement, VariableDeclarator, \
    VariableDeclaration, Resource, While, For, Variable, Assert, Empty, \
    Break, Continue, Return, Synchronized


class StatementParser(object):
    @staticmethod
    def p_block(p):
        """block : '{' block_statements_opt '}' """
        p[0] = Block(p[2])

    @staticmethod
    def p_block_statements_opt(p):
        """block_statements_opt : block_statements"""
        p[0] = p[1]

    @staticmethod
    def p_block_statements_opt2(p):
        """block_statements_opt : empty"""
        p[0] = []

    @staticmethod
    def p_block_statements(p):
        """block_statements : block_statement
                            | block_statements block_statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_block_statement(p):
        """block_statement : local_variable_declaration_statement
                           | statement
                           | class_declaration
                           | interface_declaration
                           | annotation_type_declaration
                           | enum_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_local_variable_declaration_statement(p):
        """local_variable_declaration_statement \
               : local_variable_declaration ';' """
        p[0] = p[1]

    @staticmethod
    def p_local_variable_declaration(p):
        """local_variable_declaration : type variable_declarators"""
        p[0] = VariableDeclaration(p[1], p[2])

    @staticmethod
    def p_local_variable_declaration2(p):
        """local_variable_declaration : modifiers type variable_declarators"""
        p[0] = VariableDeclaration(p[2], p[3], modifiers=p[1])

    @staticmethod
    def p_variable_declarators(p):
        """variable_declarators \
               : variable_declarator
               | variable_declarators ',' variable_declarator"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    @staticmethod
    def p_variable_declarator(p):
        """variable_declarator \
               : variable_declarator_id
               | variable_declarator_id '=' variable_initializer"""
        if len(p) == 2:
            p[0] = VariableDeclarator(p[1])
        else:
            p[0] = VariableDeclarator(p[1], initializer=p[3])

    @staticmethod
    def p_variable_declarator_id(p):
        """variable_declarator_id : NAME dims_opt"""
        p[0] = Variable(p[1], dimensions=p[2])

    @staticmethod
    def p_variable_initializer(p):
        """variable_initializer : expression
                                | array_initializer"""
        p[0] = p[1]

    @staticmethod
    def p_statement(p):
        """statement : statement_without_trailing_substatement
                     | labeled_statement
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement
                     | enhanced_for_statement"""
        p[0] = p[1]

    @staticmethod
    def p_statement_without_trailing_substatement(p):
        """statement_without_trailing_substatement \
               : block
               | expression_statement
               | assert_statement
               | empty_statement
               | switch_statement
               | do_statement
               | break_statement
               | continue_statement
               | return_statement
               | synchronized_statement
               | throw_statement
               | try_statement
               | try_statement_with_resources"""
        p[0] = p[1]

    @staticmethod
    def p_expression_statement(p):
        """expression_statement : statement_expression ';'
                                | explicit_constructor_invocation"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ExpressionStatement(p[1])

    @staticmethod
    def p_statement_expression(p):
        """statement_expression : assignment
                                | pre_increment_expression
                                | pre_decrement_expression
                                | post_increment_expression
                                | post_decrement_expression
                                | method_invocation
                                | class_instance_creation_expression"""
        p[0] = p[1]

    @staticmethod
    def p_comma_opt(p):
        """comma_opt : ','
                     | empty"""
        # ignore

    @staticmethod
    def p_array_initializer(p):
        """array_initializer : '{' comma_opt '}' """
        p[0] = ArrayInitializer()

    @staticmethod
    def p_array_initializer2(p):
        """array_initializer : '{' variable_initializers '}'
                             | '{' variable_initializers ',' '}' """
        p[0] = ArrayInitializer(p[2])

    @staticmethod
    def p_variable_initializers(p):
        """variable_initializers \
               : variable_initializer
               | variable_initializers ',' variable_initializer"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    @staticmethod
    def p_method_invocation(p):
        """method_invocation : NAME '(' argument_list_opt ')' """
        p[0] = MethodInvocation(p[1], arguments=p[3])

    @staticmethod
    def p_method_invocation2(p):
        """method_invocation \
               : name '.' type_arguments NAME '(' argument_list_opt ')'
               | primary '.' type_arguments NAME '(' argument_list_opt ')'
               | SUPER '.' type_arguments NAME '(' argument_list_opt ')' """
        p[0] = MethodInvocation(p[4], target=p[1], type_arguments=p[3],
                                arguments=p[6])

    @staticmethod
    def p_method_invocation3(p):
        """method_invocation : name '.' NAME '(' argument_list_opt ')'
                             | primary '.' NAME '(' argument_list_opt ')'
                             | SUPER '.' NAME '(' argument_list_opt ')' """
        p[0] = MethodInvocation(p[3], target=p[1], arguments=p[5])

    @staticmethod
    def p_labeled_statement(p):
        """labeled_statement : label ':' statement"""
        p[3].label = p[1]
        p[0] = p[3]

    @staticmethod
    def p_labeled_statement_no_short_if(p):
        """labeled_statement_no_short_if : label ':' statement_no_short_if"""
        p[3].label = p[1]
        p[0] = p[3]

    @staticmethod
    def p_label(p):
        """label : NAME"""
        p[0] = p[1]

    @staticmethod
    def p_if_then_statement(p):
        """if_then_statement : IF '(' expression ')' statement"""
        p[0] = IfThenElse(p[3], p[5])

    @staticmethod
    def p_if_then_else_statement(p):
        """if_then_else_statement \
               : IF '(' expression ')' statement_no_short_if ELSE statement"""
        p[0] = IfThenElse(p[3], p[5], p[7])

    @staticmethod
    def p_if_then_else_statement_no_short_if(p):
        """if_then_else_statement_no_short_if \
               : IF '(' expression ')' statement_no_short_if \
                 ELSE statement_no_short_if"""
        p[0] = IfThenElse(p[3], p[5], p[7])

    @staticmethod
    def p_while_statement(p):
        """while_statement : WHILE '(' expression ')' statement"""
        p[0] = While(p[3], p[5])

    @staticmethod
    def p_while_statement_no_short_if(p):
        """while_statement_no_short_if \
               : WHILE '(' expression ')' statement_no_short_if"""
        p[0] = While(p[3], p[5])

    @staticmethod
    def p_for_statement(p):
        """for_statement \
               : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt \
                 ')' statement"""
        p[0] = For(p[3], p[5], p[7], p[9])

    @staticmethod
    def p_for_statement_no_short_if(p):
        """for_statement_no_short_if \
               : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt \
                 ')' statement_no_short_if"""
        p[0] = For(p[3], p[5], p[7], p[9])

    @staticmethod
    def p_for_init_opt(p):
        """for_init_opt : for_init
                        | empty"""
        p[0] = p[1]

    @staticmethod
    def p_for_init(p):
        """for_init : statement_expression_list
                    | local_variable_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_statement_expression_list(p):
        """statement_expression_list : statement_expression
                                     | statement_expression_list ',' \
                                       statement_expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    @staticmethod
    def p_expression_opt(p):
        """expression_opt : expression
                          | empty"""
        p[0] = p[1]

    @staticmethod
    def p_for_update_opt(p):
        """for_update_opt : for_update
                          | empty"""
        p[0] = p[1]

    @staticmethod
    def p_for_update(p):
        """for_update : statement_expression_list"""
        p[0] = p[1]

    @staticmethod
    def p_enhanced_for_statement(p):
        """enhanced_for_statement : enhanced_for_statement_header statement"""
        p[0] = ForEach(p[1]['type'], p[1]['variable'], p[1]['iterable'], p[2],
                       modifiers=p[1]['modifiers'])

    @staticmethod
    def p_enhanced_for_statement_no_short_if(p):
        """enhanced_for_statement_no_short_if \
               : enhanced_for_statement_header statement_no_short_if"""
        p[0] = ForEach(p[1]['type'], p[1]['variable'], p[1]['iterable'], p[2],
                       modifiers=p[1]['modifiers'])

    @staticmethod
    def p_enhanced_for_statement_header(p):
        """enhanced_for_statement_header \
               : enhanced_for_statement_header_init ':' expression ')' """
        p[1]['iterable'] = p[3]
        p[0] = p[1]

    @staticmethod
    def p_enhanced_for_statement_header_init(p):
        """enhanced_for_statement_header_init : FOR '(' type NAME dims_opt"""
        p[0] = {
            'modifiers': [],
            'type': p[3],
            'variable': Variable(p[4], dimensions=p[5])
        }

    @staticmethod
    def p_enhanced_for_statement_header_init2(p):
        """enhanced_for_statement_header_init \
               : FOR '(' modifiers type NAME dims_opt"""
        p[0] = {
            'modifiers': p[3],
            'type': p[4],
            'variable': Variable(p[5], dimensions=p[6])
        }

    @staticmethod
    def p_statement_no_short_if(p):
        """statement_no_short_if : statement_without_trailing_substatement
                                 | labeled_statement_no_short_if
                                 | if_then_else_statement_no_short_if
                                 | while_statement_no_short_if
                                 | for_statement_no_short_if
                                 | enhanced_for_statement_no_short_if"""
        p[0] = p[1]

    @staticmethod
    def p_assert_statement(p):
        """assert_statement : ASSERT expression ';'
                            | ASSERT expression ':' expression ';' """
        if len(p) == 4:
            p[0] = Assert(p[2])
        else:
            p[0] = Assert(p[2], message=p[4])

    @staticmethod
    def p_empty_statement(p):
        """empty_statement : ';' """
        p[0] = Empty()

    @staticmethod
    def p_switch_statement(p):
        """switch_statement : SWITCH '(' expression ')' switch_block"""
        p[0] = Switch(p[3], p[5])

    @staticmethod
    def p_switch_block(p):
        """switch_block : '{' '}' """
        p[0] = []

    @staticmethod
    def p_switch_block2(p):
        """switch_block : '{' switch_block_statements '}' """
        p[0] = p[2]

    @staticmethod
    def p_switch_block3(p):
        """switch_block : '{' switch_labels '}' """
        p[0] = [SwitchCase(p[2])]

    @staticmethod
    def p_switch_block4(p):
        """switch_block : '{' switch_block_statements switch_labels '}' """
        p[0] = p[2] + [SwitchCase(p[3])]

    @staticmethod
    def p_switch_block_statements(p):
        """switch_block_statements \
               : switch_block_statement
               | switch_block_statements switch_block_statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_switch_block_statement(p):
        """switch_block_statement : switch_labels block_statements"""
        p[0] = SwitchCase(p[1], body=p[2])

    @staticmethod
    def p_switch_labels(p):
        """switch_labels : switch_label
                         | switch_labels switch_label"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_switch_label(p):
        """switch_label : CASE constant_expression ':'
                        | DEFAULT ':' """
        if len(p) == 3:
            p[0] = 'default'
        else:
            p[0] = p[2]

    @staticmethod
    def p_constant_expression(p):
        """constant_expression : expression"""
        p[0] = p[1]

    @staticmethod
    def p_do_statement(p):
        """do_statement : DO statement WHILE '(' expression ')' ';' """
        p[0] = DoWhile(p[5], body=p[2])

    @staticmethod
    def p_break_statement(p):
        """break_statement : BREAK ';'
                           | BREAK NAME ';' """
        if len(p) == 3:
            p[0] = Break()
        else:
            p[0] = Break(p[2])

    @staticmethod
    def p_continue_statement(p):
        """continue_statement : CONTINUE ';'
                              | CONTINUE NAME ';' """
        if len(p) == 3:
            p[0] = Continue()
        else:
            p[0] = Continue(p[2])

    @staticmethod
    def p_return_statement(p):
        """return_statement : RETURN expression_opt ';' """
        p[0] = Return(p[2])

    @staticmethod
    def p_synchronized_statement(p):
        """synchronized_statement : SYNCHRONIZED '(' expression ')' block"""
        p[0] = Synchronized(p[3], p[5])

    @staticmethod
    def p_throw_statement(p):
        """throw_statement : THROW expression ';' """
        p[0] = Throw(p[2])

    @staticmethod
    def p_try_statement(p):
        """try_statement : TRY try_block catches
                         | TRY try_block catches_opt finally"""
        if len(p) == 4:
            p[0] = Try(p[2], catches=p[3])
        else:
            p[0] = Try(p[2], catches=p[3], _finally=p[4])

    @staticmethod
    def p_try_block(p):
        """try_block : block"""
        p[0] = p[1]

    @staticmethod
    def p_catches(p):
        """catches : catch_clause
                   | catches catch_clause"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_catches_opt(p):
        """catches_opt : catches"""
        p[0] = p[1]

    @staticmethod
    def p_catches_opt2(p):
        """catches_opt : empty"""
        p[0] = []

    @staticmethod
    def p_catch_clause(p):
        """catch_clause : CATCH '(' catch_formal_parameter ')' block"""
        p[0] = Catch(p[3]['variable'], types=p[3]['types'],
                     modifiers=p[3]['modifiers'], block=p[5])

    @staticmethod
    def p_catch_formal_parameter(p):
        """catch_formal_parameter \
               : modifiers_opt catch_type variable_declarator_id"""
        p[0] = {'modifiers': p[1], 'types': p[2], 'variable': p[3]}

    @staticmethod
    def p_catch_type(p):
        """catch_type : union_type"""
        p[0] = p[1]

    @staticmethod
    def p_union_type(p):
        """union_type : type
                      | union_type '|' type"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    @staticmethod
    def p_try_statement_with_resources(p):
        """try_statement_with_resources \
               : TRY resource_specification try_block catches_opt
               | TRY resource_specification try_block catches_opt finally"""
        if len(p) == 5:
            p[0] = Try(p[3], resources=p[2], catches=p[4])
        else:
            p[0] = Try(p[3], resources=p[2], catches=p[4], _finally=p[5])

    @staticmethod
    def p_resource_specification(p):
        """resource_specification : '(' resources semi_opt ')' """
        p[0] = p[2]

    @staticmethod
    def p_semi_opt(p):
        """semi_opt : ';'
                    | empty"""
        # ignore

    @staticmethod
    def p_resources(p):
        """resources : resource
                     | resources trailing_semicolon resource"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    @staticmethod
    def p_trailing_semicolon(p):
        """trailing_semicolon : ';' """
        # ignore

    @staticmethod
    def p_resource(p):
        """resource : type variable_declarator_id '=' variable_initializer"""
        p[0] = Resource(p[2], resource_type=p[1], initializer=p[4])

    @staticmethod
    def p_resource2(p):
        """resource \
               : modifiers type variable_declarator_id '=' variable_initializer
        """
        p[0] = Resource(p[3], resource_type=p[2], modifiers=p[1],
                        initializer=p[5])

    @staticmethod
    def p_finally(p):
        """finally : FINALLY block"""
        p[0] = p[2]

    @staticmethod
    def p_explicit_constructor_invocation(p):
        """explicit_constructor_invocation \
               : THIS '(' argument_list_opt ')' ';'
               | SUPER '(' argument_list_opt ')' ';' """
        p[0] = ConstructorInvocation(p[1], arguments=p[3])

    @staticmethod
    def p_explicit_constructor_invocation2(p):
        """explicit_constructor_invocation \
               : type_arguments SUPER '(' argument_list_opt ')' ';'
               | type_arguments THIS '(' argument_list_opt ')' ';' """
        p[0] = ConstructorInvocation(p[2], type_arguments=p[1], arguments=p[4])

    @staticmethod
    def p_explicit_constructor_invocation3(p):
        """explicit_constructor_invocation \
               : primary '.' SUPER '(' argument_list_opt ')' ';'
               | name '.' SUPER '(' argument_list_opt ')' ';'
               | primary '.' THIS '(' argument_list_opt ')' ';'
               | name '.' THIS '(' argument_list_opt ')' ';' """
        p[0] = ConstructorInvocation(p[3], target=p[1], arguments=p[5])

    @staticmethod
    def p_explicit_constructor_invocation4(p):
        """explicit_constructor_invocation \
               : primary '.' type_arguments SUPER '(' argument_list_opt ')' ';'
               | name '.' type_arguments SUPER '(' argument_list_opt ')' ';'
               | primary '.' type_arguments THIS '(' argument_list_opt ')' ';'
               | name '.' type_arguments THIS '(' argument_list_opt ')' ';' """
        p[0] = ConstructorInvocation(p[4], target=p[1], type_arguments=p[3],
                                     arguments=p[6])

    @staticmethod
    def p_class_instance_creation_expression(p):
        """class_instance_creation_expression \
               : NEW type_arguments class_type '(' argument_list_opt ')' \
                 class_body_opt"""
        p[0] = InstanceCreation(p[3], type_arguments=p[3], arguments=p[5],
                                body=p[7])

    @staticmethod
    def p_class_instance_creation_expression2(p):
        """class_instance_creation_expression \
               : NEW class_type '(' argument_list_opt ')' class_body_opt"""
        p[0] = InstanceCreation(p[2], arguments=p[4], body=p[6])

    @staticmethod
    def p_class_instance_creation_expression3(p):
        """class_instance_creation_expression \
               : primary '.' NEW type_arguments class_type \
                 '(' argument_list_opt ')' class_body_opt"""
        p[0] = InstanceCreation(p[5], enclosed_in=p[1], type_arguments=p[4],
                                arguments=p[7], body=p[9])

    @staticmethod
    def p_class_instance_creation_expression4(p):
        """class_instance_creation_expression \
               : primary '.' NEW class_type '(' argument_list_opt ')' \
                 class_body_opt"""
        p[0] = InstanceCreation(p[4], enclosed_in=p[1], arguments=p[6],
                                body=p[8])

    @staticmethod
    def p_class_instance_creation_expression5(p):
        """class_instance_creation_expression \
               : class_instance_creation_expression_name NEW class_type \
                 '(' argument_list_opt ')' class_body_opt"""
        p[0] = InstanceCreation(p[3], enclosed_in=p[1], arguments=p[5],
                                body=p[7])

    @staticmethod
    def p_class_instance_creation_expression6(p):
        """class_instance_creation_expression \
               : class_instance_creation_expression_name NEW \
                 type_arguments class_type '(' argument_list_opt ')' \
                 class_body_opt"""
        p[0] = InstanceCreation(p[4], enclosed_in=p[1], type_arguments=p[3],
                                arguments=p[6], body=p[8])

    @staticmethod
    def p_class_instance_creation_expression_name(p):
        """class_instance_creation_expression_name : name '.' """
        p[0] = p[1]

    @staticmethod
    def p_class_body_opt(p):
        """class_body_opt : class_body
                          | empty"""
        p[0] = p[1]

    @staticmethod
    def p_field_access(p):
        """field_access : primary '.' NAME
                        | SUPER '.' NAME"""
        p[0] = FieldAccess(p[3], p[1])

    @staticmethod
    def p_array_access(p):
        """array_access \
               : name '[' expression ']'
               | primary_no_new_array '[' expression ']'
               | array_creation_with_array_initializer '[' expression ']' """
        p[0] = ArrayAccess(p[3], p[1])

    @staticmethod
    def p_array_creation_with_array_initializer(p):
        """array_creation_with_array_initializer \
               : NEW primitive_type dim_with_or_without_exprs array_initializer
               | NEW class_or_interface_type dim_with_or_without_exprs \
                 array_initializer"""
        p[0] = ArrayCreation(p[2], dimensions=p[3], initializer=p[4])

    @staticmethod
    def p_dim_with_or_without_exprs(p):
        """dim_with_or_without_exprs \
               : dim_with_or_without_expr
               | dim_with_or_without_exprs dim_with_or_without_expr"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_dim_with_or_without_expr(p):
        """dim_with_or_without_expr : '[' expression ']'
                                    | '[' ']' """
        if len(p) == 3:
            p[0] = None
        else:
            p[0] = p[2]

    @staticmethod
    def p_array_creation_without_array_initializer(p):
        """array_creation_without_array_initializer \
               : NEW primitive_type dim_with_or_without_exprs
               | NEW class_or_interface_type dim_with_or_without_exprs"""
        p[0] = ArrayCreation(p[2], dimensions=p[3])