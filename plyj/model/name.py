from operator import attrgetter
from plyj.model.source_element import SourceElement


class Name(SourceElement):
    simple = property(attrgetter("_simple"))
    value = property(attrgetter("_value"))

    def __init__(self, value):
        """
        Represents a name.
        :param value: The name.
        """
        super(Name, self).__init__()
        self._fields = ['value']

        assert isinstance(value, str)

        self._value = value
        self._simple = "." not in value

    def append_name(self, name):
        self._simple = False
        if isinstance(name, Name):
            self._value = self._value + '.' + name._value
        else:
            self._value = self._value + '.' + name

    @staticmethod
    def ensure(se, simple):
        if isinstance(se, str):
            return Name(se)
        if not isinstance(se, Name):
            assert False
        if simple and not se.simple:
            assert se.simple
        return se