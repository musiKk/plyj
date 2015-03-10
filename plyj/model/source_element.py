#!/usr/bin/env python2
from ply.lex import LexToken


IGNORE_KEYS = {'tokens', '_fields'}


class SourceElement(object):
    """
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    """

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []
        self.tokens = []

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        if not isinstance(other, SourceElement):
            return False
        my_keys = set(self.__dict__.keys()) - IGNORE_KEYS
        your_keys = set(other.__dict__.keys()) - IGNORE_KEYS

        if my_keys != your_keys:
            return False

        for key in my_keys:
            if self.__dict__[key] != other.__dict__[key]:
                return False

        return True

    def __ne__(self, other):
        return not self == other

    def add_tokens_right(self, other):
        assert isinstance(other, SourceElement)
        self.tokens.extend(other.tokens)
        other.tokens = []

    def add_tokens_left(self, other):
        assert isinstance(other, SourceElement)
        other.tokens.extend(self.tokens)
        self.tokens = other.tokens
        other.tokens = []

    def accept(self, visitor):
        """
        default implementation that visit the subnodes in the order
        they are stored in self_field
        """
        class_name = self.__class__.__name__
        visit = getattr(visitor, 'visit_' + class_name)
        if visit(self):
            for f in self._fields:
                field = getattr(self, f)
                if field:
                    if isinstance(field, list):
                        for elem in field:
                            if isinstance(elem, SourceElement):
                                elem.accept(visitor)
                    elif isinstance(field, SourceElement):
                        field.accept(visitor)
        getattr(visitor, 'leave_' + class_name)(self)


class AnonymousSourceElement(SourceElement):
    """
    This is a SourceElement that does not warrant its own class. Before it was
    added, values would be passed around as strings, integers, dicts or other
    primitive types when there was no real need to add another class to wrap
    them. These primitive types have no room to store the tokens from the
    Java source, so AnonymousSourceElement was added to wrap these values and
    provide room to store the tokens that created them.
    """
    def __init__(self, value):
        super(AnonymousSourceElement, self).__init__()
        self._fields = ['value']
        self.value = value


def extract_tokens(source_element, from_element):
    if isinstance(from_element, AnonymousSourceElement):
        source_element.add_tokens_right(from_element)
        return from_element.value
    return from_element


def ensure_se(value):
    """
    Used in many model classes to ensure that a particular parameter is a
    SourceElement (for consistency)
    :param value: The value to make into an AnonymousSourceElement if it isn't
                  a SourceElement
    :return: A SourceElement
    """
    if not isinstance(value, SourceElement):
        return AnonymousSourceElement(value)
    return value


def collect_tokens(p):
    """
    Takes the PLY Parser state and then puts all tokens it can find into the
    parser result (p[0]).
    :param p: Parser state
    :return: None
    """
    if p[0] is None:
        raise ValueError("The result of the rule is probably not None. "
                         "Explicitly specify p[0] = "
                         "AnonymousSourceElement(None) to silence this"
                         "warning")
    # in_after is True if we have passed p[0] and are now appending to
    # tokens_after. In many production rules, p[0] is set to p[n]. So we should
    # prepend the tokens that appear before p[n] rather than appending them
    # (hence we make two lists).
    in_after = False
    tokens_before = []  # Tokens that appear before p[0]
    tokens_after = []  # Tokens that appear after p[0]
    for i, t in enumerate(p.slice):
        if p[i] is p[0] and i != 0:
            in_after = True
        if isinstance(t, LexToken):
            if in_after:
                tokens_after.append(t)
            else:
                tokens_before.append(t)

    # Turn the parser result into an AnonymousSourceElement or if it already is
    # a SourceElement, add the tokens to the current element.
    if isinstance(p[0], SourceElement):
        tokens_before.extend(p[0].tokens)
        tokens_before.extend(tokens_after)
        p[0].tokens = tokens_before
    else:
        tokens_before.extend(tokens_after)
        p[0] = AnonymousSourceElement(p[0])
        p[0].tokens = tokens_before


class Statement(SourceElement):
    pass


class Expression(SourceElement):
    def __init__(self):
        super(Expression, self).__init__()
        self._fields = []