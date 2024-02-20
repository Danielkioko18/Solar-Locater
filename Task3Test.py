import os
import itertools
import string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# setting up node class for binary search tree
class Node:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
        self.left = None
        self.right = None


# the binary search tree class
class BST:
    # initializing bst class
    def __init__(self):
        self.root = None

    # insert username, hashed_passwrod
    def insert(self, username, hashed_password):
        self.root = self._insert(self.root, username, hashed_password)

    # insert username, hashed_password and node to the tree
    def _insert(self, node, username, hashed_password):
        if node is None:
            return Node(username, hashed_password)
        if username < node.username:
            node.left = self._insert(node.left, username, hashed_password)
        else:
            node.right = self._insert(node.right, username, hashed_password)
        return node
    # searching
    def search(self, username):
        return self._search(self.root, username)

    def _search(self, node, username):
        if node is None or node.username == username:
            return node
        if username < node.username:
            return self._search(node.left, username)
        return self._search(node.right, username)


# hashing the randomly generated password  for brute force in type2 file
def hash_password(password, salt):
    salted_password = salt + password.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=100000,
        length=32
    )
    hashed_password = kdf.derive(salted_password)
    return hashed_password

# function to load the password file into the program
def load_password_file(filename):
    bst = BST()
    with open(filename, 'r') as file:
        for line in file:
            username, hashed_password = line.strip().split('-')
            bst.insert(username, hashed_password)
    return bst


# function to define the order of traversal in the binary search tree
def in_order_traversal(node, result):
    if node:
        in_order_traversal(node.left, result)
        result.append(node.username)
        in_order_traversal(node.right, result)


# function to crack the password from the loaded password file
def crack_password(password_file, max_password_length):
    passwords = load_password_file(password_file)
    usernames = []
    in_order_traversal(passwords.root, usernames)

    # itterating through the password file and the
    for length in range(1, max_password_length + 1):
        for candidate in itertools.product(string.ascii_lowercase, repeat=length):
            candidate_password = ''.join(candidate)

            for username in usernames:
                stored_password = passwords.search(username)
                hashed_candidate = hash_password(candidate_password, os.urandom(1))
                if hashed_candidate.hex() == stored_password.hashed_password:
                    print(f"Password for user '{username}' is: {candidate_password}")
                    return

    print("Password not found in the specified length range.")


if __name__ == "__main__":
    password_file = input("Enter the path to the password file (type 2): ")
    max_password_length = int(input("Enter the maximum password length to crack: "))
    print("\nCracking password........................................")

    crack_password(password_file, max_password_length)