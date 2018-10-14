# encoding: utf-8
import hashlib

def hash_str(val, salt=''):
    """Hash a string
    :param some_val: str to write
    :param salt: salt to append to string
    :returns the .digest() of the hash
    Example::
        hash_str('world!', salt='hello, ').hex()[:6] == '68e656'
    """

    # create a SHA256 hash object
    h = hashlib.sha256()
    try:
        # check if salt is a string object 
        if isinstance(salt, str):
            # feed h with bytes which is salted in utf-8
            h.update(str.encode(salt))
        else:
            # nothing will change
            h.update(salt)
    except AttributeError:
        raise

    # feed h with bytes which is in utf-8
    h.update(str.encode(val))

    # return h digest value
    return h.digest()

