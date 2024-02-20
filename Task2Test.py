from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
import os
import random
import string


def generate_random_password(length):
    # Generate a random password of a given length
    characters = string.ascii_lowercase
    return ''.join(random.choice(characters) for _ in range(length))


def generate_usernames_and_passwords(num_accounts, min_password_length, max_password_length):
    usernames = []
    plaintext_passwords = []
    hashed_passwords = []
    salted_passwords = []

    for i in range(num_accounts):
        username = f"usr{random.randint(1000000, 9999999)}"
        password_length = random.randint(min_password_length, max_password_length)
        password = generate_random_password(password_length)

        salt = os.urandom(1)
        password_bytes = password.encode('utf-8')

        # Generate plaintext passwords
        plaintext_passwords.append(f"{username} {password}")

        # Generate hashed passwords
        salted_password = salt + password_bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=salt,
            iterations=100000,
            length=32
        )
        hashed_password = kdf.derive(salted_password)
        hashed_passwords.append(f"{username} {hashed_password.hex()}")

        # Generate salted and hashed passwords
        salted_passwords.append(f"{username} {salt.hex()} {hashed_password.hex()}")

    return usernames, plaintext_passwords, hashed_passwords, salted_passwords


def write_to_files(filename, data):
    with open(filename, 'w') as file:
        file.write("\n".join(data))


def main():
    num_accounts = 100
    min_password_length = 3
    max_password_length = 8

    usernames, plaintext_passwords, hashed_passwords, salted_passwords = generate_usernames_and_passwords(
        num_accounts, min_password_length, max_password_length)

    # Write data to files
    write_to_files('plaintext_passwords.txt', plaintext_passwords)
    write_to_files('hashed_passwords.txt', hashed_passwords)
    write_to_files('salted_passwords.txt', salted_passwords)


if __name__ == "__main__":
    main()