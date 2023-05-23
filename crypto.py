import hashlib
from Crypto.Cipher import AES

def pad_text(text):
    # Determine the number of bytes needed to pad the text
    num_bytes = AES.block_size - (len(text) % AES.block_size)

    # Pad the text with null bytes
    padded_text = text + ('0' * num_bytes)

    return padded_text



def encrypt_text(key, text):
    # Pad the text to a multiple of 16 bytes
    padded_text = text.encode('utf-8')
    padded_text += b"\0" * (AES.block_size - len(padded_text) % AES.block_size)

    key_padded = pad_text(key)
    print(key_padded, len(key_padded))


    # Create a new AES cipher using the key and IV
    # iv = hashlib.md5(key.encode('utf-8')).digest()
    cipher = AES.new(key_padded.encode('utf-8'), AES.MODE_ECB)

    # Encrypt the padded text
    encrypted_text = cipher.encrypt(padded_text)

    # Return the encrypted text as a base64-encoded string
    return encrypted_text.hex()

def decrypt_text(key, ciphertext):
    # Convert the ciphertext from a hexadecimal string to bytes
    ciphertext = bytes.fromhex(ciphertext)

    key_padded = pad_text(key)

    # Create a new AES cipher using the key and IV
    # iv = hashlib.md5(key.encode('utf-8')).digest()
    cipher = AES.new(key_padded.encode('utf-8'), AES.MODE_ECB)

    # Decrypt the ciphertext and remove the padding
    decrypted_text = cipher.decrypt(ciphertext).rstrip(b"\0")

    # Return the decrypted text as a string
    return decrypted_text.decode('utf-8')

# # Example usage:
key = "mysecretkey"
text = "Hello, World!"
# encrypted_text = encrypt_text(key, text)
# print(encrypted_text)
# print("------------")
# print(key)
# decrypted_text = decrypt_text(key, encrypted_text)
# print(decrypted_text)
