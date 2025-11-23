from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt_data(plaintext:str, key) -> bytes:
    '''
    ## Encrypt Data
     Encrypts plaintext using AES-CFB mode.
    
     Code generated with the assistance of the Google Gemini AI model.
     Prompt Used: Python example of a simple encryptor and decryptor using cryptography
     Date Accessed: 2025-11-22

    * **plaintext** [str]: the message to encrypt
    * **key** [bytes]: the PSK to use for encryption.

    **returns** [bytes]: the encoded message
    '''
    # Generate a unique Initialization Vector (IV) for this message
    iv = os.urandom(16) 
    
    # Create a cipher object in encrypt mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the payload bytes
    payload_bytes = plaintext.encode("utf-8")
    encrypted_bytes = encryptor.update(payload_bytes) + encryptor.finalize()

    # For transmission, we combine IV and ciphertext, then Base64 encode the result
    combined_payload = iv + encrypted_bytes
    return base64.b64encode(combined_payload)