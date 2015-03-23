#!/usr/bin/env python2
import abc
from operator import attrgetter
from ply.lex import LexToken


IGNORE_KEYS = {'tokens', '_fields'}


class SourceElement(object):
    """
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.

    The "tokens" field is a dictionary of lists. Each key in the dictionary
    should be the name of an attribute to which these tokens are related.
    For example, a function call will have a key called "arguments" in its
    "tokens" dictionary which will consist of the comma tokens that separate
    arguments.

    The "_fields" field is a dictionary of
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []
        self.tokens = {}

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        """
        Unfortunately, we hit Python's built in recursion limit on some files
        in the JDK7. So we're going to have to work around it by using a stack
        of some kind.
        :param other:
        :return:
        """
        class StackItem:
            def __init__(self, compare_left, compare_right, compare_iterator):
                self.compare_left = compare_left
                self.compare_right = compare_right
                self.compare_iterator = compare_iterator

        stack = [StackItem(self, other, None)]

        while len(stack) > 0:
            left = stack[-1].compare_left
            right = stack[-1].compare_right
            iterator = stack[-1].compare_iterator

            if iterator is None:
                # Set up the iterator
                if not isinstance(other, SourceElement):
                    return False
                if type(left) != type(right):
                    return False

                left_keys = set(left.__dict__.keys()) - IGNORE_KEYS
                right_keys = set(right.__dict__.keys()) - IGNORE_KEYS

                if left_keys != right_keys:
                    return False

                iterator = stack[-1].compare_iterator = left_keys.__iter__()

            for key in iterator:
                if key.startswith("_"):
                    continue  # Ignore private attributes.
                # Check everything unless it is a SourceElement
                left_element = left.__dict__[key]
                right_element = right.__dict__[key]
                if type(left_element) != type(right_element):
                    return False

                if isinstance(left_element, SourceElement):
                    stack.append(StackItem(left_element, right_element, None))
                    break
                else:
                    if left_element != right_element:
                        return False
            else:
                stack.pop()

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

    def _alter_tokens(self, name, ase, clear_if_not_ase=True):
        """
        Sets the tokens for a particular group from an abstract syntax element.
        If ase is NOT an AnonymousSE, the tokens for that group are cleared if
        clear_if_not_ase is True.

        For more information, see the SourceElement class docstring.
        :type ase: AnonymousSE
        :type name: str
        :param name: The token group to replace
        :param ase: The anonymous syntax element to take the tokens from
        :return: If ase is an AnonymousSE, "ase.value". Otherwise ase.
        """
        if isinstance(ase, AnonymousSE):
            if "" in ase.tokens:
                self.tokens[name] = ase.tokens[""]
                assert len(ase.tokens) == 1  # Only has un-grouped ("") tokens.
            return ase.value
        if clear_if_not_ase:
            self.tokens[name] = []
        return ase

    def _absorb_ase_tokens(self, ase):
        """
        Shortcut to _alter_tokens(ase)
        """
        return self._alter_tokens("", ase)

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
            raise TypeError("list_ is not a list (got " + str(list_) + ")")
        for i in range(len(list_)):
            if map_func is not None:
                list_[i] = map_func(list_[i])
            if not isinstance(list_[i], class_or_type_or_tuple):
                raise TypeError("list_[i] is a {}, not a {} as required."
                                .format(str(type(list_[i])),
                                        str(class_or_type_or_tuple)))
        return list_

    def add_tokens_right(self, other):
        assert isinstance(other, AnonymousSE)
        if "" not in other.tokens:
            return
        if "" in self.tokens:
            self.tokens[""].extend(other.tokens[""])
        else:
            self.tokens[""] = other.tokens[""]
        other.tokens[""] = []

    def add_tokens_left(self, other):
        assert isinstance(other, AnonymousSE)
        if "" not in other.tokens:
            return
        if "" in self.tokens:
            other.tokens[""].extend(self.tokens[""])
        else:
            self.tokens[""] = other.tokens[""]
        other.tokens[""] = []

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
    """
    This is a SourceElement that does not warrant its own class. Before it was
    added, values would be passed around as strings, integers, dicts or other
    primitive types when there was no real need to add another class to wrap
    them. These primitive types have no room to store the tokens from the
    Java source, so AnonymousSE was added to wrap these values and
    provide room to store the tokens that created them.
    """

    def serialize(self):
        return str(self.value)

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
        if "" in p[0].tokens:
            tokens_before.extend(p[0].tokens[""])
        tokens_before.extend(tokens_after)
        p[0].tokens[""] = tokens_before
    else:
        tokens_before.extend(tokens_after)
        p[0] = AnonymousSE(p[0])
        p[0].tokens[""] = tokens_before


class Statement(SourceElement):
    __metaclass__ = abc.ABCMeta
    statement_label = property(attrgetter("_statement_label"))

    def __init__(self):
        super(Statement, self).__init__()
        self._statement_label = None

    @statement_label.setter
    def statement_label(self, statement_label):
        from plyj.model.name import Name
        self._statement_label = Name.ensure(statement_label, True)

    @abc.abstractmethod
    def statement_serialize(self):
        """
        Instead of implementing serialize, please implement this instead. That
        way you'll get the added benefit of the label stuff being automatically
        done for you.
        """
        pass

    def serialize(self):
        if self.statement_label is None:
            return self.statement_serialize()
        else:
            return (self.statement_label.serialize() + ": " +
                    self.statement_serialize())


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