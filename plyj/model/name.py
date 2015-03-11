from plyj.model.source_element import SourceElement

__author__ = 'matthew'


class Name(SourceElement):
    def __init__(self, value, simple=False):
        """
        Represents a name.
        :param value: The name.
        :param simple: A simple name never has a dot.
        """
        super(Name, self).__init__()
        self._fields = ['value']

        assert isinstance(value, str)
        assert isinstance(simple, bool)
        if simple:
            assert "." not in value

        self.value = value
        self.simple = simple

    def append_name(self, name):
        assert not self.simple
        if hasattr(name, "value") and isinstance(name.value, str):
            self.value = self.value + '.' + name.value
        else:
            self.value = self.value + '.' + name