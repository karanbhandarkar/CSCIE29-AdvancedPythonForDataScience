# encoding: utf-8
import contextlib
import os.path
import unittest

if __name__ == '__main__':
    # python direct run uses the form of import statement
    from pset_utils.io import atomic_write
else:
    # pytest uses the this form of import statement
    from .io import atomic_write

class AtomicWriteTestCase(unittest.TestCase):

    def test_atomic_write(self):
        filename = "hello.txt"

        with contextlib.suppress(FileNotFoundError):
           os.remove(filename)

        with atomic_write(filename) as f:
            f.write("world!")

        self.assertTrue(os.path.isfile(filename))

    def test_contents(self):
        filename = "hello.txt"
        
        if os.path.isfile(filename):
            with open(filename) as f:
                contents = f.read()
                self.assertEqual(contents, "world!")
           
            remove_files(filename)


def remove_files(*args):
    """Helper function for use by main.py, tests
    Checks if file is present and deletes it if so
    :param *args: one or more filenames as str
    """
    for filename in args:
        if os.path.isfile(filename):
            os.remove(filename)


if __name__ == '__main__':
    #
    # old way of unit test 
    #
    # test atomic write
    remove_files('hello.txt')
    
    filename = "hello.txt"
    with atomic_write(filename) as f:
        f.write("world!")
    
    remove_files(filename)
