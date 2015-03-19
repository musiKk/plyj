from plyj.model.source_element import AnonymousSE, Expression, \
    StatementNoPostfixSemicolon, Declaration, Statement


def assert_none_or_ensure(x, class_or_type_or_tuple, *ensure_args):
    """
    :param x: An object
    :param class_or_type_or_tuple: Second argument to isinstance. Must have an
                                   "ensure(x)" static method
    :return: None or a object of one of the passed types.
    """
    try:
        if x is None:
            return None
        x = class_or_type_or_tuple.ensure(x, *ensure_args)
        assert isinstance(x, class_or_type_or_tuple)
        return x
    except:
        raise  # Put a breakpoint here ;)


def assert_none_or(x, class_or_type_or_tuple):
    """
    Shortcut to:
        assert x is None or isinstance(x, class_or_type_or_tuple)
    :param x: An object
    :param class_or_type_or_tuple: Second argument to isinstance
    :return: x
    """
    if x is None:
        return x
    return assert_type(x, class_or_type_or_tuple)


def assert_type(x, class_or_type_or_tuple):
    """
    Shortcut to:
        assert isinstance(x, class_or_type_or_tuple)
    :param x: An object
    :param class_or_type_or_tuple: Second argument to isinstance
    :return: x
    """
    try:
        if not isinstance(x, class_or_type_or_tuple):
                raise TypeError("x is a {}, not a {} as required."
                                .format(str(type(x)),
                                        str(class_or_type_or_tuple)))
        return x
    except:
        raise  # Put a breakpoint here ;)


def serialize_type_parameters(type_parameters):
    """
    :param type_parameters: A list of TypeParameter objects
    :return: A string:
             0 Parameters: ""
             1 Parameter:  "<ABC abc>"
             2 Parameters: "<ABC abc, DEF def>"
             ...
    """
    type_parameters = [x.serialize() for x in type_parameters]
    type_parameters = ", ".join(type_parameters)
    if len(type_parameters) > 0:
        type_parameters = "<" + type_parameters + ">"
    return type_parameters


def serialize_extends(extends):
    if extends is None:
        return ""
    elif isinstance(extends, list):
        return "extends " + "".join([x.serialize() + " " for x in extends])
    else:
        return "extends " + extends.serialize() + " "


def serialize_implements(implements):
    if len(implements) == 0:
        return ""
    else:
        implements = [x.serialize() for x in implements]
        return "implements " + ", ".join(implements) + " "


def indent(string):
    return "\n".join(["    " + x for x in string.split("\n")])


"""
def needs_semicolon(x):
    if isinstance(x, Statement):
        return not isinstance(x, StatementNoPostfixSemicolon)
    elif not isinstance(x, Declaration):
        # Make sure we've check that this isn't a statement first.
        # VariableDeclarationStatement is both a declaration and a
        # statement, but it requires a postfix seimcolon
        return True
"""

def serialize_body(body, default="{}"):
    if len(body) == 0:
        return default
    else:
        result = "{\n"
        for statement in body:
            result += indent(statement.serialize())
            result += "\n"
        result += "}"
        return result


def serialize_modifiers(modifiers):
    return "".join([x.serialize() + " " for x in modifiers])


def serialize_parameters(parameters):
    if len(parameters) == 0:
        return "()"
    else:
        parameters = [x.serialize() for x in parameters]
        return "(" + ", ".join(parameters) + ")"


def serialize_type_arguments(type_arguments):
    if len(type_arguments) == 0:
        return ""
    elif type_arguments == "diamond":
        return "<>"
    else:
        for x in type_arguments:
            if isinstance(x, str):
                print type_arguments
        return "<" + ", ".join([x.serialize() for x in type_arguments]) + ">"


def serialize_arguments(arguments):
    if arguments is None:
        return "()"
    else:
        return "(" + ", ".join([x.serialize() for x in arguments]) + ")"


def serialize_dimensions(dimensions):
    if isinstance(dimensions, AnonymousSE):
        dimensions = dimensions.value
    if isinstance(dimensions, int):
        return "[]" * dimensions
    assert isinstance(dimensions, list)
    assert len(dimensions) > 0
    for d in dimensions:
        assert d is None or isinstance(d, Expression)
    result = ""
    for dimension in dimensions:
        if dimension is None:
            result += "[]"
        else:
            result += "[" + dimension.serialize() + "]"
    return result