plyj [![Build Status](https://secure.travis-ci.org/musiKk/plyj.png?branch=master)](http://travis-ci.org/musiKk/plyj)
====

plyj is a Java 7 parser written in Python. It has the awesome [PLY] as its sole dependency.

Status
------

**plyj is officially in maintenance mode.** For the foreseeable future no new developments will be made by me. As explained below plyj is basically a manual transcription of JDT's grammar. This has served me well in the past but with the Java 8 features JDT's developers did some things I'm unable to reproduce with PLY. I'm not smart enough to do this on my own. Writing parsers is still black magic to me. I am not thrilled by this development.

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

Contributions
-------------

Contributions are always welcome. Depending on the type of work it may
take a little while until I get around to accepting them.

* commit test that demonstrates a bug (optional)
* commit the fix
* open pull request

The test is required but does *not* have to be provided by you. If you
do provide it, committing it first shows appropriate messages in the
pull request and makes it easier to accept via Web.

Performance
-----------

A word of caution: Since plyj is pure Python, it is quite slow. Based on my laptop (which has an i7-3517U @ 1.90 GHz) I can present the following numbers (running inside a virtual machine):

* 619 rules
* 1149 states
* ~3.28 seconds to compile the grammar
* java/util/Collections.java takes ~0.44 seconds to parse (it's quite big though)

The timings are obviously highly dependent on the used hardware. My old laptop (Core 2 Duo @ 1 GHz) took 17 and 1.8 seconds respectively.

History
-------

### 0.2 (in development)

* added `ExpressionStatement`

### 0.1 (2014-12-25) - The Christmas Release

* initial release
* supports complete Java 7 syntax (minus bugs)

[PLY]: https://github.com/dabeaz/ply
[Java Development Tools]: http://www.eclipse.org/jdt/
