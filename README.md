plyj [![Build Status](https://secure.travis-ci.org/musiKk/plyj.png?branch=master)](http://travis-ci.org/musiKk/plyj)
====

plyj is a Java parser written in Python. It has the awesome [PLY] as its sole dependency.

Synopsis
--------

```python
import plyj.parser as plyj

parser = plyj.Parser()

# parse a compilation unit from a file
tree = parser.parse_file(file('/foo/bar/Baz.java'))

# parse a compilation unit from a string
tree = parser.parse_string('class Foo { }')

# parse expression from string
tree = parser.parse_expression('1 / 2 * (float) 3')

# slightly bigger example: parse from an installed JDK with sources
import zipfile
srczip = zipfile.ZipFile('/usr/lib/jvm/java-6-openjdk/src.zip', mode='r')
info = srczip.getinfo('java/lang/Object.java')
srcfile = srczip.open(info)
tree = parser.parse_file(srcfile)
```

Acknowledgement
---------------

plyj is more or less a 1:1 translation of the grammar used in the [Java Development Tools] for Eclipse.

Completeness
------------

The grammar is complete. There may still be errors left though. It successfully parsed every source file of the Oracle JDK. A lot of bugs were found that way but for all I know there may be many more. Time will tell.

Performance
-----------

A word of caution: Since plyj is pure Python (and I mean 100% from front to back), it is quite slow. Based on my old laptop (which usually runs with 1 GHz) I can present the following numbers:

* 619 rules
* 1149 states
* ~17 seconds to compile the grammar
* java/util/Collections.java takes ~1.8 seconds to parse (it's quite big though)

[PLY]: https://github.com/dabeaz/ply
[Java Development Tools]: http://www.eclipse.org/jdt/
