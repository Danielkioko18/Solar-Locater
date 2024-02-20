from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(serialized_key):
    return serialization.load_pem_public_key(serialized_key, backend=default_backend())

def encrypt_asymmetric(public_key, data):
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_asymmetric(private_key, ciphertext):
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext_bytes

def encrypt_symmetric(key, data):
    cipher = Cipher(
        algorithm=algorithms.AES(key),
        mode=modes.CFB(b'\0' * 16),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return ciphertext

def decrypt_symmetric(key, ciphertext):
    cipher = Cipher(
        algorithm=algorithms.AES(key),
        mode=modes.CFB(b'\0' * 16),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def hash_data(data):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    if isinstance(data, str):
        digest.update(data.encode('utf-8'))
    else:
        digest.update(data)
    return digest.finalize()

def main():
    # Generate key pair for asymmetric encryption
    private_key, public_key = generate_key_pair()

    # Serialize public key for encryption
    serialized_public_key = serialize_public_key(public_key)

    # Deserialize public key for decryption
    deserialized_public_key = deserialize_public_key(serialized_public_key)

    # Read plaintext data from input file
    with open('input.txt', 'r') as file:
        plaintext_data = file.read()

    # Encrypt data with symmetric encryption
    symmetric_key = os.urandom(32)
    ciphertext_symmetric = encrypt_symmetric(symmetric_key, plaintext_data)

    # Encrypt symmetric key with asymmetric encryption
    encrypted_symmetric_key = encrypt_asymmetric(deserialized_public_key, symmetric_key)

    # Combine encrypted data and hash value
    encrypted_data = ciphertext_symmetric + encrypted_symmetric_key
    hash_value = hash_data(plaintext_data)
    encrypted_data += hash_value

    # Save encrypted data to output file
    with open('output.txt', 'wb') as file:
        file.write(encrypted_data)

    # Read encrypted data from output file
    with open('output.txt', 'rb') as file:
        received_data = file.read()

    # Separate encrypted data and hash value
    hash_size = 32  # Assuming SHA256 hash size
    key_size = private_key.key_size // 8  # Size of the RSA key in bytes

    received_ciphertext = received_data[:-hash_size - key_size]  # ciphertext + RSA key size
    received_encrypted_symmetric_key = received_data[-hash_size - key_size:-hash_size]  # RSA key size
    received_hash_value = received_data[-hash_size:]  # hash size

    # Decrypt symmetric key with asymmetric decryption
    decrypted_symmetric_key = decrypt_asymmetric(private_key, received_encrypted_symmetric_key)

    # Decrypt data with symmetric decryption
    decrypted_data = decrypt_symmetric(decrypted_symmetric_key, received_ciphertext)

    # Save decrypted data to output file
    with open('output.txt', 'w') as file:
        file.write(decrypted_data.decode('utf-8'))

    # Verify data integrity
    received_hash = hash_data(decrypted_data)

    if received_hash == received_hash_value:
        print("Data integrity verified. Decrypted data:", decrypted_data)
    else:
        print("Data integrity verification failed.")

if __name__ == "__main__":
    main()