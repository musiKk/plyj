import os
import subprocess
import unittest

# OpenJDK9 does not yet work due to new language features (lambda functions)
import sys
from plyj.parser import Parser

MERCURIAL_REPO_LOCATION = "http://hg.openjdk.java.net/jdk7/jdk7"
DOWNLOAD_FOLDER = "openjdk7"

EXCEPTIONS = [
    # Has a mistake in it :( Missing semicolon on line 119
    "jdk7/jdk/test/java/util/WeakHashMap/GCDuringIteration.java",
    # Not syntactically correct java?? Contains "\t" in source (not in string)
    "jdk7/langtools/test/com/sun/javadoc/testSourceTab/DoubleTab/C.java",
    "jdk7/langtools/test/com/sun/javadoc/testSourceTab/SingleTab/C.java",
    "jdk7/langtools/test/com/sun/javadoc/testUnnamedPackage/BadSource.java",
    "jdk7/langtools/test/com/sun/javadoc/testSupplementary/C.java",
    "jdk7/langtools/test/tools/javac/ExtraneousEquals.java",
    "jdk7/langtools/test/tools/javadoc/6964914/JavacWarning.java",
    "jdk7/langtools/test/tools/javadoc/6964914/Error.java",
    "jdk7/langtools/test/tools/javadoc/sourceOption/p/A.java",
    "jdk7/langtools/test/tools/javadoc/T4994049/FileWithTabs.java",
    "jdk7/langtools/test/tools/javac/typeAnnotations/newlocations/BasicTest.java",
    "jdk7/langtools/test/tools/javac/diags/examples/ProcessorWrongType/ProcessorWrongType.java",
    "jdk7/langtools/test/tools/javac/diags/examples/DefaultAllowedInIntfAnnotationMember.java",
    # The following files are assumed to be bad and haven't been manually
    # checked
    "jdk7/langtools/test/tools/javac/diags/examples/AssertAsIdentifier.java",
    "jdk7/langtools/test/tools/javac/diags/examples/FinallyWithoutTry.java",
    "jdk7/langtools/test/tools/javac/diags/examples/IllegalStartOfExpr.java",
    "jdk7/langtools/test/tools/javac/diags/examples/CannotCreateArrayWithTypeArgs.java",
    "jdk7/langtools/test/tools/javac/diags/examples/EnumAsIdentifier.java",
    "jdk7/langtools/test/tools/javac/diags/examples/IllegalLineEndInCharLit.java",
    "jdk7/langtools/test/tools/javac/diags/examples/AssertAsIdentifier2.java",
    "jdk7/langtools/test/tools/javac/diags/examples/TryWithoutCatchOrFinally.java",
    "jdk7/langtools/test/tools/javac/diags/examples/TryWithoutCatchOrFinallyOrResource.java",
    "jdk7/langtools/test/tools/javac/diags/examples/Expected3.java",
    "jdk7/langtools/test/tools/javac/diags/examples/PrematureEOF.java",
    "jdk7/langtools/test/tools/javac/diags/examples/DotClassExpected.java",
    "jdk7/langtools/test/tools/javac/diags/examples/MalformedFpLit.java",
    "jdk7/langtools/test/tools/javac/diags/examples/AnnotationMustBeNameValue.java",
    "jdk7/langtools/test/tools/javac/diags/examples/ElseWithoutIf.java",
    "jdk7/langtools/test/tools/javac/diags/examples/IllegalNonAsciiDigit.java",
    "jdk7/langtools/test/tools/javac/diags/examples/IntfMethodCantHaveBody.java",
    "jdk7/langtools/test/tools/javac/diags/examples/InvalidHexNumber.java",
    "jdk7/langtools/test/tools/javac/diags/examples/IllegalChar.java",
    "jdk7/langtools/test/tools/javac/diags/examples/TypeReqClassArray.java",
    "jdk7/langtools/test/tools/javac/diags/examples/UnclosedComment.java",
    "jdk7/langtools/test/tools/javac/diags/examples/EnumAsIdentifier2.java",
    "jdk7/langtools/test/tools/javac/diags/examples/ThrowsNotAllowedInAnno.java",
    "jdk7/langtools/test/tools/javac/diags/examples/CatchWithoutTry.java",
    "jdk7/langtools/test/tools/javac/diags/examples/Expected2.java",
    "jdk7/langtools/test/tools/javac/diags/examples/Orphaned.java",
    "jdk7/langtools/test/tools/javac/generics/6413682/T6413682.java",
    "jdk7/langtools/test/tools/javac/policy/test3/A.java",
    "jdk7/langtools/test/tools/javac/annotations/neg/Z2.java",
    "jdk7/langtools/test/tools/javac/annotations/neg/Z3.java",
    "jdk7/langtools/test/tools/javac/annotations/neg/Z13.java",
    "jdk7/langtools/test/tools/javac/annotations/neg/AnnComma.java",
    "jdk7/langtools/test/tools/javac/annotations/neg/Syntax1.java",
    "jdk7/langtools/test/tools/javac/failover/FailOver01.java",
    "jdk7/langtools/test/tools/javac/6440583/A.java",
    "jdk7/langtools/test/tools/javac/javazip/bad/B.java",
    "jdk7/langtools/test/tools/javac/tree/T6963934.java",
    "jdk7/langtools/test/tools/javac/tree/TestAnnotatedAnonClass.java",
    "jdk7/langtools/test/tools/javac/rawDiags/Error.java",
    "jdk7/langtools/test/tools/javac/quid/T6999438.java",
    "jdk7/langtools/test/tools/javac/TryWithResources/BadTwrSyntax.java",
    "jdk7/langtools/test/tools/javac/TryWithResources/PlainTry.java",
    "jdk7/langtools/test/tools/javac/unicode/NonasciiDigit.java",
    "jdk7/langtools/test/tools/javac/unicode/SupplementaryJavaID1.java",
    "jdk7/langtools/test/tools/javac/unicode/UnicodeAtEOL.java",
    "jdk7/langtools/test/tools/javac/unicode/UnicodeCommentDelimiter.java",
    "jdk7/langtools/test/tools/javac/unicode/SupplementaryJavaID6.java",
    "jdk7/langtools/test/tools/javac/unicode/SupplementaryJavaID4.java",
    "jdk7/langtools/test/tools/javac/unicode/SupplementaryJavaID5.java",
    "jdk7/langtools/test/tools/javac/unicode/SupplementaryJavaID2.java",
    "jdk7/langtools/test/tools/javac/unicode/FirstChar2.java",
    "jdk7/langtools/test/tools/javac/unicode/NonasciiDigit2.java",
    "jdk7/langtools/test/tools/javac/unicode/SupplementaryJavaID3.java",
    "jdk7/langtools/test/tools/javac/api/T6265137a.java",
    "jdk7/langtools/test/tools/javac/enum/6384542/T6384542a.java",
    "jdk7/langtools/test/tools/javac/enum/6384542/T6384542.java",
    "jdk7/langtools/test/tools/javac/DefiniteAssignment/ConstantInfiniteWhile.java",
    "jdk7/langtools/test/tools/javac/processing/6994946/SyntaxErrorTest.java",
    "jdk7/langtools/test/tools/javac/processing/errors/TestParseErrors/ParseErrors.java",
    "jdk7/langtools/test/tools/javac/6302184/T6302184.java",
    "jdk7/langtools/test/tools/javac/T4994049/T4994049.java",
    "jdk7/langtools/test/tools/javac/4846262/Test.java",
    "jdk7/langtools/test/tools/javac/ParseConditional.java",
    "jdk7/langtools/test/tools/javac/LabeledDeclaration.java",
    "jdk7/langtools/test/tools/javac/Digits.java",
    "jdk7/langtools/test/tools/javac/Parens2.java",
    "jdk7/langtools/test/tools/javac/EOI.java",
    "jdk7/langtools/test/tools/javac/Parens3.java",
    "jdk7/langtools/test/tools/javac/T6882235.java",
    "jdk7/langtools/test/tools/javac/ExtendArray.java",
]


def _should_skip(file_name):
    for e in EXCEPTIONS:
        if file_name.replace("\\", "/").endswith(e):
            return True
    return False


class MercurialNotFoundError(Exception):
    pass


class ShNotFoundError(Exception):
    pass


class OpenJDK7Test(unittest.TestCase):
    def download_openjdk7(self):
        if os.path.exists(DOWNLOAD_FOLDER):
            print ("OpenJDK7 already cloned. If this failed, please delete "
                   "the folder \"{}\". ".format(DOWNLOAD_FOLDER))
            print ("Skipping download of OpenJDK7")
        else:
            os.mkdir(DOWNLOAD_FOLDER)

            print("Cloning Mercurial repository at \"{}\" into \"{}\"".format(
                MERCURIAL_REPO_LOCATION, DOWNLOAD_FOLDER))

            # Thanks Sven Marnach! https://stackoverflow.com/questions/11210104
            try:
                params = ["hg", "clone", MERCURIAL_REPO_LOCATION]
                subprocess.call(params, cwd=DOWNLOAD_FOLDER)
            except OSError as e:
                if e.errno == os.errno.ENOENT:
                    raise MercurialNotFoundError(
                        "Mercurial is not installed or the `hg` command is "
                        "otherwise unavailable. Install mercurial and make "
                        "sure `hg` is on your path.")
                raise

            print("OpenJDK7 Cloned successfully. Getting source...")

            # Now we need to follow the instructions in the readme (run
            # ./get_source.sh)
            try:
                params = ["sh", "./get_source.sh"]
                cwd = os.path.join(DOWNLOAD_FOLDER, "jdk7")
                subprocess.call(params, cwd=cwd)
            except OSError as e:
                if e.errno == os.errno.ENOENT:
                    raise ShNotFoundError(
                        "The `sh` command is unavailable. Install Cygwin if "
                        "running on Windows and ensure sh.exe is in your "
                        "\"Path\" environment variable.")
                raise

    def find_java_files(self):
        retn = []
        # Thanks ghostdog74 https://stackoverflow.com/questions/3964681
        for root, dirs, files in os.walk(DOWNLOAD_FOLDER):
            for f in files:
                if f.endswith(".java"):
                     retn.append(os.path.join(root, f))
        return retn

    def test_openjdk7(self):
        self.download_openjdk7()
        java_files = self.find_java_files()

        p = Parser()
        for i, java_file in enumerate(java_files):
            percent = i / float(len(java_files)) * 100.0
            if _should_skip(java_file):
                continue
            sys.stdout.write('[{:.1f}%] \"{}\": '.format(percent, java_file))
            sys.stdout.flush()

            parse_result = p.parse_file(java_file)
            self.assertIsNotNone(parse_result)
            parse_string = parse_result.serialize()
            parse_result2 = p.parse_string(parse_string)
            self.assertIsNotNone(parse_result2)
            self.assertEqual(parse_result, parse_result2)

            sys.stdout.write("OK\n")