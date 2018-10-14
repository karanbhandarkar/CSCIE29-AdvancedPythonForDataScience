# encoding: utf-8
from pset_utils.hashing import hash_str
from pset_utils.io import atomic_write

def main(gh_username):
    """
    Return hash in hex of user's lowercase Github username using CSCI_SALT
    Examples:
        main("gorlins")
        '9a895b7f8e92cad816973ea92fb96545fba02a578e9fb8f684e8a12cf500b750'
    """
    CSCI_SALT = bytes.fromhex(
        "d4 b5 1b 2a 6c e0 2b b8 e8 29 ce 45 18 b0 f9 c0"
        "a8 f4 ec 6b 59 36 01 89 b1 be 69 26 1e 05 75 bc"
        )
    
    return hash_str(gh_username.lower(), salt=CSCI_SALT).hex()
    
if __name__ == "__main__":
    print("Hash of Github username gorlins: ", main("gorlins"))

    with atomic_write("hello.txt") as f:
        f.write("world!")
