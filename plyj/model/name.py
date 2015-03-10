from plyj.model.source_element import SourceElement

__author__ = 'matthew'


class Name(SourceElement):

    def __init__(self, value):
        super(Name, self).__init__()
        self._fields = ['value']
        assert isinstance(value, str)
        self.value = value

    def append_name(self, name):
        if hasattr(name, "value") and isinstance(name.value, str):
            self.value = self.value + '.' + name.value
        else:
            self.value = self.value + '.' + name