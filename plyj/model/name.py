from operator import attrgetter
from plyj.model.source_element import Expression
from plyj.utility import assert_type


class Name(Expression):
    simple = property(attrgetter("_simple"))
    value = property(attrgetter("_value"))

    def serialize(self):
        return self.value

    def __init__(self, value):
        """
        Represents a name.
        :param value: The name.
        """
        super(Name, self).__init__()
        self._fields = ['value']

        self._value = assert_type(value, str)
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
            raise TypeError("Required Name, got \"{}\"".format(str(type(se))))
        if simple and not se.simple:
            raise TypeError("Required simple Name, got complex Name")
        return se