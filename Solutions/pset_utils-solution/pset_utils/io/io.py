# encoding: utf-8
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager

@contextmanager
def atomic_write(file, mode='w', as_file=True, **kwargs):
    """Write a file atomically
    :param file: str or :class:`os.PathLike` target to write
    :param bool as_file:  if True, the yielded object is a :class:File.
        Otherwise, it will be the temporary file path string
    :param kwargs: anything else needed to open the file
    :raises: FileExistsError if target exists
    This function uses the python `tempfile` module to create a temporary file. 
    This insures that the destination file will not exist unless the file has been 
    written completely.
    Example::
        with atomic_write("hello.txt") as f:
            f.write("world!")
    """
    if os.path.isfile(file):
        raise FileExistsError
    else:
        fname, fext = os.path.splitext(file)
        # mkstemp() creates a temporary file in the most secure manner possible
        # mkstemp() returns a tuple containing an OS-level handle to an open file 
        # (as would be returned by os.open()) and the absolute pathname of that 
        # file, in that order.
        fd, tmp = tempfile.mkstemp(suffix=fext, text=True)
        try:
            with os.fdopen(fd, mode) as f:
                yield f
            # recursively move tmp to file
            shutil.move(tmp, file)
            tmp = None
        finally:
            if (tmp is not None):
                try:
                    os.unlink(tmp)
                except:
                    pass

