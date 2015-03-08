class TokenCarrier(object):
    def __init__(self, value, tokens):
        self.value = value
        self.tokens = tokens


class StringTokenCarrier(TokenCarrier):
    def __init__(self, p, index):
        super(StringTokenCarrier, self).__init__(p[index], p.slice[index])