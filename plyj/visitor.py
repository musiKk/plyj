#!/usr/bin/env python2


class Visitor(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __getattr__(self, name):
        if not (name.startswith('visit_') or name.startswith('leave_')):
            raise AttributeError('name must start with visit_ or leave_ but'
                                 ' was {}'.format(name))

        def f(element):
            if self.verbose:
                msg = 'unimplemented call to {}; ignoring ({})'
                print(msg.format(name, element))
            return True
        return f