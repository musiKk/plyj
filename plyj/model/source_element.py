#!/usr/bin/env python2


class SourceElement(object):
    """
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    """

    def __init__(self, tokens=None):
        super(SourceElement, self).__init__()
        self._fields = []
        self.tokens = tokens or []

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

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