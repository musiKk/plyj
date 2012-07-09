plyj
====

plyj is a Java parser written in Python using PLY. It has the awesome [PLY] as its sole dependency.

Acknowledgement
--------------

plyj is more or less a 1:1 translation of the grammar used in the [Java Development Tools] for Eclipse. It really takes someone smarter than me to create a parser of that caliber. That's no false modesty. After many failed attempts of writing the parser using only the [Java Language Specification] I just gave up.

Completeness
-----------

The grammar is complete. There may still be errors left though. It successfully parsed every source file of the Oracle JDK. A lot of bugs were found that way but for all I know there may be many more. Time will tell.

The DOM is in a very rough shape and will be the next point on my list. It is just enough to guide the development process but not really usable on its own as many parts are missing completely.

Performance
----------

A word of caution: Since plyj is pure Python, it is quite slow. Based on my old laptop (which usually runs with 1 GHz) I can present the following numbers:

* 619 rules
* 1149 states
* ~17 seconds to compile the grammar
* java/util/Collections.java takes ~1.8 seconds to parse (it's quite big though)

[PLY]: https://github.com/dabeaz/ply
[Java Development Tools]: http://www.eclipse.org/jdt/
[Java Language Specification]: http://docs.oracle.com/javase/specs/
