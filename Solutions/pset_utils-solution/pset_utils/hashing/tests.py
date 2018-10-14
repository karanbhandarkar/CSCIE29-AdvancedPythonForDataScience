# encoding: utf-8
import unittest

if __name__ == '__main__':
    from hashing import hash_str
else:
    from .hashing import hash_str

class HashingTestCase(unittest.TestCase):
    CSCI_SALT = bytes.fromhex(
        "d4 b5 1b 2a 6c e0 2b b8 e8 29 ce 45 18 b0 f9 c0"
        "a8 f4 ec 6b 59 36 01 89 b1 be 69 26 1e 05 75 bc"
        )
    
    def test_helloworld(self):
        h1 = hash_str('world!', salt='hello, ').hex()[:6]
        self.assertEqual(h1, "68e656")

    def test_gorlins(self):
        h2 = hash_str("gorlins", salt=self.CSCI_SALT).hex()
        self.assertEqual(h2, "9a895b7f8e92cad816973ea92fb96545fba02a578e9fb8f684e8a12cf500b750")

if __name__ == '__main__':
    #
    # The old way of unit test
    #
    # test hash_str() #1
    h1 = hash_str('world!', salt='hello, ').hex()[:6]
    print(h1)
