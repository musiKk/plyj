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
    else:
        return "extends " + extends.serialize() + " "


def serialize_implements(implements):
    if len(implements) == 0:
        return ""
    else:
        implements = [x.serialize() for x in implements]
        return "implements " + ", ".join(implements) + " "


def serialize_body(body):
    if len(body) == 0:
        return "{}"
    else:
        body = ["    " + x.serialize() for x in body]
        return "{\n" + ";\n".join(body) + "\n}\n"