from operator import attrgetter
from plyj.model.source_element import Modifier
from plyj.utility import assert_type


class BasicModifier(Modifier):
    value = property(attrgetter("_value"))

    def serialize(self):
        return self.value

    def __init__(self, value=None):
        """
        Represents a name.
        :param value: The name.
        """
        super(BasicModifier, self).__init__()
        self._fields = ['value']

        self._value = None

        self.value = value

    @value.setter
    def value(self, value):
        assert BasicModifier.is_basic_modifier(value)
        self._value = assert_type(value, str)

    @staticmethod
    def ensure_modifier(se):
        if isinstance(se, str):
            return BasicModifier(se)
        assert isinstance(se, Modifier)
        return se

    @staticmethod
    def set_visibility(modifier_list, new_visibility):
        for x in modifier_list:
            if (isinstance(x, BasicModifier) and
               x.value in ["protected", "public", "private"]):
                x.value = new_visibility
                return
        # Couldn't find visibility specifier.
        modifier_list.append(BasicModifier(new_visibility))

    @staticmethod
    def is_basic_modifier(string):
        return string in ["public", "protected", "private", "static",
                          "abstract", "final", "native", "synchronized",
                          "transient", "volatile", "strictfp"]