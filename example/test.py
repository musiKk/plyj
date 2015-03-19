#!/usr/bin/env python2
import os

from plyj.parser import Parser

DOWNLOAD_FOLDER = "/home/matthew/Documents/Swig"


def find_java_files():
    retn = []
    # Thanks ghostdog74 https://stackoverflow.com/questions/3964681
    for root, dirs, files in os.walk(DOWNLOAD_FOLDER):
        for f in files:
            if f.endswith(".java"):
                 retn.append(os.path.join(root, f))
    return retn

p = Parser()
for f in find_java_files():
    print "Parsing " + f
    parse = p.parse_file(f)

    print "Serializing " + f
    serialized = parse.serialize()
    with open("test.java", "w") as j:
        j.write(serialized)

    print "Parsing (2) " + f
    parse2 = p.parse_file("test.java")

    print "Asserting " + f
    assert parse == parse2