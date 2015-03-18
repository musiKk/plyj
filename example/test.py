#!/usr/bin/env python2

from plyj.parser import Parser

p = Parser()
parse = p.parse_file("/home/matthew/Documents/Swig/Examples/test-suite/java/enum_thorough_proper_runme.java")

serialized = parse.serialize()
with open("test.java", "w") as j:
    j.write(serialized)

