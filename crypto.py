# Hybrid cryptosystem with hash based integrity verification

# import necessary python libraries for cryptography
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


'''
this function generates a key_pair  
with public exponent of 65537 and key size of 2048
'''
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key # returns both private and public keys


'''
    function to generate a serial public key
    returns serialized public key
'''
def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


'''
    function to deserialize the public key generated in the above key
    the function  takes serialized key as a parameter
'''
def deserialize_PK(serialized_key):
    return serialization.load_pem_public_key(serialized_key, backend=default_backend())


'''
    function to encrypt the data obtained from the input file by asymmetric algorithms
    the function takes the public key and data reasd from the file as parameters
    returns the ciphertext
'''
def encrypt_asymmetric(public_key, data):
    print("Input for asymmetric encryption:", data,"\n")

    #convertig data to ciphertext asymmetrically
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # print the output of asymmetric encryption
    print("Output of asymmetric encryption:\n")
    print(ciphertext.hex(), "\n")
    return ciphertext

'''
    function to decrypt the output of the asymetric data encryption.
    the function takes the public key and the cipertext as parameters
    returns plaintext in byte form
'''
def decrypt_asymmetric(private_key, ciphertext):
    # prints the input to the Asymmetric decryption
    print("Input for asymmetric decryption:\n")
    print(ciphertext.hex(), "\n")

    # obtaining the plaintext from the encrypted text symmetrically.
    pt_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    #print the output of the asymmetric decryption.
    print("Output of asymmetric decryption:\n")
    print(pt_bytes, "\n")
    return pt_bytes

'''
    function to encrypt data symmetrically 
    the function takes as parameters key and data
'''
def encrypt_symmetric(key, data):
    #prints the input to the symetric encryption
    print("Input for symmetric encryption:\n")
    print(data, "\n")
    # generate cipher
    cipher = Cipher(
        algorithm=algorithms.AES(key),
        mode=modes.CFB(b'\0' * 16),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    # getting the ciphertext
    ciphertxt = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    #print output from the symetric encryption
    print("Output of symmetric encryption:\n", ciphertxt.hex())
    return ciphertxt # return the ciphertext



'''
    function to decrypt the output of the symetric data encryption.
    the function takes the key and the ciphertext as parameters
'''

def decrypt_symmetric(key, ciphertext):
    #printing the input into the symetric decryption
    print("Input for symmetric decryption:\n")
    print(ciphertext.hex(),"\n")

    cipher = Cipher(
        algorithm=algorithms.AES(key),
        mode=modes.CFB(b'\0' * 16),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    #getting the plaintext
    plainT = decryptor.update(ciphertext) + decryptor.finalize()
    #printing the output from the symetric encryption
    print("Output of symmetric decryption:\n")
    print(plainT.decode('utf-8'), "\n")
    return plainT


'''
    this is the hash functio which is used to veriy the integrity of the data
    generates a hash representation which is used for comparison to test integrity
'''
def hash_function(data):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    if isinstance(data, str):
        digest.update(data.encode('utf-8'))
    else:
        digest.update(data)
    return digest.finalize()


'''
    main function which implements all the functions that we have defined fomthe code above
    since the code is designe in a modular form
'''
def main():
    #get input file from the user
    input_file = input("Enter the name of the file you want to encrypt: \n")

    # Generating a key pair from generate_key_pair function
    private_key, public_key = generate_key_pair()

    # Serializing the public key for encryption purpose
    serialized_PK = serialize_public_key(public_key)

    #output the serialized public key
    print("Serialized public key:\n")
    print(serialized_PK.decode('utf-8'), "\n")

    # deserializing the public key for decryption purpose
    deserialized_PK= deserialize_PK(serialized_PK)

    # Reading the plaintext data from the input file
    with open(input_file, 'r') as file:
        plaintext_D = file.read()
    print("Plaintext data:\n", plaintext_D, "\n")

    # Encryption of data with symmetric encryption
    sym_key= os.urandom(32) # generating byteform data for encryption
    ciphertext_symmetric = encrypt_symmetric(sym_key, plaintext_D)

    # encrypting symetric key with asymetric key
    encr_PK= encrypt_asymmetric(deserialized_PK, sym_key)

    # combining of encrypted data with the hash value
    encr_data = ciphertext_symmetric + encr_PK
    hash_val = hash_function(plaintext_D)
    encr_data += hash_val

    # saving the encrypted data into the output file
    with open('output.txt', 'wb') as file:
        file.write(encr_data)

    # reading encrypted data from the output file
    with open('output.txt', 'rb') as file:
        received_data = file.read()

    # Separating encrypted data from the hash values
    hash_sz = 32  # HA256 hash size
    key_size = private_key.key_size // 8  # RSA key size in bytes

    received_ct = received_data[:-hash_sz - key_size]  # ciphertext + RSA key size
    received_encr_sym_key = received_data[-hash_sz - key_size:-hash_sz]  # RSA key size
    received_hash_val = received_data[-hash_sz:]  # hash size

    # Decrypting the symmetric key with asymmetric decryption
    decrypted_sym_key = decrypt_asymmetric(private_key, received_encr_sym_key)

    # Decrypting data with symmetric decryption
    decrypted_data = decrypt_symmetric(decrypted_sym_key, received_ct)

    # Saving decrypted data to output file
    with open('output.txt', 'w') as file:
        file.write(decrypted_data.decode('utf-8'))

    # Verifying  data integrity using the hash functionality
    rec_hash = hash_function(decrypted_data)

    # checking for integrity of the data using if statements
    if rec_hash == received_hash_val:
        print("Data integrity verified. The data received is not tempered.\n")
        print("Decrypted output:\n")
        print(decrypted_data,"\n")
    else:
        print("Data integrity verification failed!! The data was tempered with")

    #displaying the number of characters in input plaintext, ciphertext, and final decrypted plaintext for accuracy
    # Display the number of characters in plaintext
    print(f"Number of characters in plaintext: {len(plaintext_D)}")
    # Display the number of characters in ciphertext
    print(f"Number of characters in ciphertext: {len(encr_data)}")
    # Display the number of characters in decrypted plaintext
    print(f"Number of characters in output plaintext: {len(decrypted_data)}")


if __name__ == "__main__":
    main()