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
    try:
        assert x is None or isinstance(x, class_or_type_or_tuple)
        return x
    except:
        raise  # Put a breakpoint here ;)


def assert_type(x, class_or_type_or_tuple):
    """
    Shortcut to:
        assert isinstance(x, class_or_type_or_tuple)
    :param x: An object
    :param class_or_type_or_tuple: Second argument to isinstance
    :return: x
    """
    try:
        assert isinstance(x, class_or_type_or_tuple)
        return x
    except:
        raise  # Put a breakpoint here ;)