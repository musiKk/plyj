import os
import subprocess
import unittest

MERCURIAL_REPO_LOCATION = "http://hg.openjdk.java.net/jdk7/jdk7"
DOWNLOAD_FOLDER = "openjdk7"


class MercurialNotFoundError(Exception):
    pass


class ShNotFoundError(Exception):
    pass


class StatementTest(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DOWNLOAD_FOLDER):
            print ("OpenJDK7 already cloned. If this failed, please delete "
                   "the folder \"{}\". ".format(DOWNLOAD_FOLDER))
            print ("Skipping download of OpenJDK7")
        else:
            os.mkdir(DOWNLOAD_FOLDER)

            print "Cloning Mercurial repository at \"{}\" into \"{}\"".format(
                MERCURIAL_REPO_LOCATION, DOWNLOAD_FOLDER)

            # Thanks Sven Marnach! https://stackoverflow.com/questions/11210104
            try:
                params = ["hg", "clone",
                          "http://hg.openjdk.java.net/jdk7/jdk7"]
                subprocess.call(params, cwd=DOWNLOAD_FOLDER)
            except OSError as e:
                if e.errno == os.errno.ENOENT:
                    raise MercurialNotFoundError(
                        "Mercurial is not installed or the `hg` command is "
                        "otherwise unavailable. Install mercurial and make "
                        "sure `hg` is on your path.")
                raise

            print "OpenJDK7 Cloned successfully. Getting source..."

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

    def test_while(self):
        pass