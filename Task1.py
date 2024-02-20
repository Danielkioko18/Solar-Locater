import hashlib

# Function to create a password hash
def create_password_hash(password, salt):
    password = password.encode() + salt
    password_hash = hashlib.sha256(password).hexdigest()
    return password_hash

# Function to register a user
def register_user(username, password, salt, plaintext_file, hashed_file, salted_file):
    with open(plaintext_file, "a") as plaintext, open(hashed_file, "a") as hashed, open(salted_file, "a") as salted:
        plaintext.write(f"{username}:{password}\n")
        hashed_password = create_password_hash(password, salt)
        hashed.write(f"{username}:{hashed_password}\n")
        salted_password = create_password_hash(password, salt)
        salted.write(f"{username}:{salt.decode()}:{salted_password}\n")

# Function to authenticate a user
def authenticate_user(username, password, plaintext_file, hashed_file, salted_file):
    with open(plaintext_file, "r") as plaintext, open(hashed_file, "r") as hashed, open(salted_file, "r") as salted:
        plaintext_verified = False
        hashed_verified = False
        salted_verified = False

        for line in plaintext:
            parts = line.strip().split(":")
            if parts[0] == username and parts[1] == password:
                plaintext_verified = True

        for line in hashed:
            parts = line.strip().split(":")
            if parts[0] == username:
                stored_hashed_password = parts[1]
                hashed_password = create_password_hash(password, salted)
                if stored_hashed_password == hashed_password:
                    hashed_verified = True

        for line in salted:
            parts = line.strip().split(":")
            if parts[0] == username:
                stored_salt = parts[1].encode()
                stored_hashed_password = parts[2]
                salted_password = create_password_hash(password, stored_salt)
                if stored_hashed_password == salted_password:
                    salted_verified = True

        return plaintext_verified, hashed_verified, salted_verified

# Main program
def main():
    plaintext_file = "plaintext_passwords.txt"
    hashed_file = "hashed_passwords.txt"
    salted_file = "salted_passwords.txt"

    while True:
        print("1. Create Account")
        print("2. Authenticate")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            username = input("Enter your username (up to 10 alphabetic characters): ").strip()[:10]
            password = input(f"Enter your password (lowercase letters only): ")
            salt = input("Enter a one-byte salt: ").encode()

            register_user(username, password, salt, plaintext_file, hashed_file, salted_file)
            print("Account created successfully!")

        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            plaintext_verified, hashed_verified, salted_verified = authenticate_user(username, password, plaintext_file, hashed_file, salted_file)

            if plaintext_verified:
                print("Username and password verified in plaintext file.")
            if hashed_verified:
                print("Username and password verified in hashed file.")
            if salted_verified:
                print("Username and password verified in salted file.")

            if not (plaintext_verified or hashed_verified or salted_verified):
                print("Authentication failed.")

        else:
            print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()