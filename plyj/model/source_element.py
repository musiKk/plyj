#!/usr/bin/env python2
import abc
from operator import attrgetter
from ply.lex import LexToken


IGNORE_KEYS = {'tokens', '_fields'}


class SourceElement(object):
    """
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    """
    __metaclass__ = abc.ABCMeta

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
        if type(other) != type(self):
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

    @abc.abstractmethod
    def serialize(self):
        pass

    def _assert_body(self, body):
        from plyj.model.annotation import AnnotationDeclaration
        from plyj.model.classes import ClassDeclaration
        from plyj.model.enum import EnumDeclaration
        from plyj.model.interface import InterfaceDeclaration

        return self._assert_list(body, (Statement,
                                        ClassDeclaration,
                                        InterfaceDeclaration,
                                        AnnotationDeclaration,
                                        EnumDeclaration))

    def _absorb_ase_tokens(self, ase):
        """
        Absorbs all the tokens in the passed AnonymousSE. If it isn't an
        AnonymousSE, ignore it and return ase. If it is actually an
        AnonymousSE, move the tokens into this SourceElement and return
        ase.value
        """
        if isinstance(ase, AnonymousSE):
            self.add_tokens_right(ase)
            return ase.value
        return ase

    def _assert_list_ensure(self, list_, class_):
        """
        Shortcut to assert_list(list_, class_, class_.ensure)
        """
        return self._assert_list(list_, class_, class_.ensure)

    def _assert_list(self, list_, class_or_type_or_tuple, map_func=None):
        """
        Runs various assertions on a list.
        :param list_: The list of objects. If None, [] is assumed instead.
        :param class_or_type_or_tuple: A tuple of types. If any item in this
                                       list is not one of these types, an
                                       TypeError is raised. This argument is
                                       passed directly to isinstance
        :param map_func: If this is not None, every item in the list becomes
                         the return value of this function when each item is
                         passed to the function as its first and only argument.
        :return: A list of objects that are only of the types in
                 class_or_type_or_tuple. If list_ is None, [] is returned.
        """
        if list_ is None:
            # Default argument to new list fallback.
            return []
        list_ = self._absorb_ase_tokens(list_)
        if isinstance(list_, class_or_type_or_tuple):
            # Mistake: Needed a list of X, but got X instead.
            return [list_]
        if not isinstance(list_, list):
            raise TypeError("list_ is not a list")
        for i in range(len(list_)):
            if map_func is not None:
                list_[i] = map_func(list_[i])
            if not isinstance(list_[i], class_or_type_or_tuple):
                raise TypeError("list_[i] is a {}, not a {} as required."
                                .format(str(type(list_[i])),
                                        str(class_or_type_or_tuple)))
        return list_

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
        Default implementation that visits the sub-nodes in the order they are
        stored in self._field
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


class AnonymousSE(SourceElement):
    def serialize(self):
        return str(self.value)

    """
    This is a SourceElement that does not warrant its own class. Before it was
    added, values would be passed around as strings, integers, dicts or other
    primitive types when there was no real need to add another class to wrap
    them. These primitive types have no room to store the tokens from the
    Java source, so AnonymousSE was added to wrap these values and
    provide room to store the tokens that created them.
    """
    def __init__(self, value):
        super(AnonymousSE, self).__init__()
        self._fields = ['value']
        self.value = value

    @staticmethod
    def ensure(value):
        """
        Used in many model classes to ensure that a particular parameter is a
        SourceElement (for consistency)
        :param value: The value to make into an AnonymousSE if it isn't
                      a SourceElement
        :return: A SourceElement
        """
        if not isinstance(value, AnonymousSE):
            if isinstance(value, SourceElement):
                raise ValueError("Cannot convert to AnonymousSE since it is "
                                 "already a SourceElement")
            if isinstance(value, list):
                raise ValueError("List tokens should be absorbed")
            return AnonymousSE(value)
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
                         "Explicitly specify p[0] = AnonymousSE(None) to "
                         "silence this warning")
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

    # Turn the parser result into an AnonymousSE or if it already is
    # a SourceElement, add the tokens to the current element.
    if isinstance(p[0], SourceElement):
        tokens_before.extend(p[0].tokens)
        tokens_before.extend(tokens_after)
        p[0].tokens = tokens_before
    else:
        tokens_before.extend(tokens_after)
        p[0] = AnonymousSE(p[0])
        p[0].tokens = tokens_before


class Statement(SourceElement):
    __metaclass__ = abc.ABCMeta
    label = property(attrgetter("_label"))

    @abc.abstractmethod
    def statement_serialize(self):
        """
        Instead of implementing serialize, please implement this instead. That
        way you'll get the added benefit of the label stuff being automatically
        done for you.
        """
        pass

    def serialize(self):
        if self.label is None:
            return self.statement_serialize()
        else:
            return self.label.serialize() + ": " + self.statement_serialize()

    def __init__(self):
        super(Statement, self).__init__()
        self._label = None

    def set_label(self, label):
        from plyj.model.name import Name
        self._label = Name.ensure(label, True)


class StatementNoPostfixSemicolon(Statement):
    @abc.abstractmethod
    def statement_serialize(self):
        pass


class Expression(SourceElement):
    @abc.abstractmethod
    def serialize(self):
        pass


class Declaration(SourceElement):
    """
    Something acceptable to find within the body of a class
    """
    @abc.abstractmethod
    def serialize(self):
        pass


class Modifier(SourceElement):
    @abc.abstractmethod
    def serialize(self):
        pass