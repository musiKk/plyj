#!/usr/bin/env python2

from plyj.parser import Parser

p = Parser()
parse = p.parse_file("/home/matthew/Documents/plyj/openjdk7/jdk7/jdk/src/share/classes/sun/nio/cs/SingleByte.java")

serialized = parse.serialize()
with open("test.java", "w") as j:
    j.write(serialized)

parse2 = p.parse_file("test.java")

assert parse == parse2