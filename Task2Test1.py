from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
import os
import random
import string

def generate_password(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

def generate_username():
    prefix = "usra"
    suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    return prefix + suffix

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

def create_account(username_range, password_range, num_accounts):
    accounts = []
    for _ in range(num_accounts):
        username = generate_username()
        password = generate_password(random.randint(password_range[0], password_range[1]))
        accounts.append((username, password))
    return accounts

def create_password_file(filename, accounts, file_type):
    with open(filename, 'w') as file:
        for username, password in accounts:
            if file_type == 'plain':
                file.write(f"{username}-{password}\n")
            elif file_type == 'hashed':
                salt = os.urandom(1)
                hashed_password = hash_password(password, salt)
                file.write(f"{username}-{hashed_password.hex()}\n")
            elif file_type == 'salted':
                salt = os.urandom(1)
                hashed_password = hash_password(password, salt)
                file.write(f"{username}-{salt.hex()}-{hashed_password.hex()}\n")

# Prompt for password and account ranges
password_length_min = int(input("Enter minimum password length: "))
password_length_max = int(input("Enter maximum password length: "))
num_accounts = int(input("Enter the number of accounts: "))

# Generate accounts and create separate password files
for i in range(1, 4):  # Creating 3 separate password files
    username_password_pairs = create_account((password_length_min, password_length_max), (password_length_min, password_length_max), num_accounts)
    file_type = 'plain' if i == 1 else 'hashed' if i == 2 else 'salted'
    create_password_file(f"password_file{i}.txt", username_password_pairs, file_type)

print(f"Password files created with {num_accounts} accounts each.")