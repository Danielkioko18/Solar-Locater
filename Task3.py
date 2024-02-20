from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import itertools
import string


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


def load_password_file(filename):
    passwords = {}
    with open(filename, 'r') as file:
        for line in file:
            username, password = line.strip().split('-')
            passwords[username] = password
    return passwords


def crack_password(password_file, max_password_length):
    passwords = load_password_file(password_file)

    for length in range(1, max_password_length + 1):
        for candidate in itertools.product(string.ascii_lowercase, repeat=length):
            candidate_password = ''.join(candidate)

            for username, hashed_password in passwords.items():
                hashed_candidate = hash_password(candidate_password, os.urandom(1))
                if hashed_candidate.hex() == hashed_password:
                    print(f"Password for user '{username}' is: {candidate_password}")
                    return

    print("Password not found in the specified length range.")
    print(username)


if __name__ == "__main__":
    password_file = input("Enter the path to the password file (type 2): ")
    max_password_length = int(input("Enter the maximum password length to crack: "))

    crack_password(password_file, max_password_length)