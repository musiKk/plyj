#!/usr/bin/env python2

from plyj.parser import Parser

p = Parser()
parse = p.parse_file("")

serialized = parse.serialize()
with open("test.java", "w") as j:
    j.write(serialized)

