import serial
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
from configparser import ConfigParser

def decrypt_data(encoded_payload, key) -> str:
    '''
    ## Encrypt Data
     Encrypts plaintext using AES-CFB mode.
    
     Code generated with the assistance of the Google Gemini AI model.
     Prompt Used: Python example of a simple encryptor and decryptor using cryptography
     Date Accessed: 2025-11-22

    * **encoded_payload** []: the base64 encoded encrypted message
    * **key** [bytes]: the PSK used for decryption

    '''
    # Decode Base64 string back to bytes
    combined_bytes = base64.b64decode(encoded_payload)

    # Extract the IV (first 16 bytes) and the actual ciphertext
    iv = combined_bytes[:16]
    ciphertext = combined_bytes[16:]

    # Create a cipher object in decrypt mode using the same key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_bytes.decode('utf-8')


def capture():
    '''
    ## Capture
    Set up and read transmissions from drone
    '''
    
    output = config.get('Files','OUTPUT_FILE')
    port = config.get('Bluetooth','PORT')
    baud_rate = config.getint('Bluetooth','BAUD')
    if config.get('Encryption','KEY') != None:
        key = config.get('Encryption','KEY')
        key = base64.b64decode(key)

    print(f"Opening Bluetooth serial port {port} ")

    # Initialize serial port object
    ser = serial.Serial(
        port=port,
        baudrate=baud_rate,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=None 
    )
    capturing = False
    try:
        if ser.isOpen():
            print("Port opened successfully. Waiting for data...")
            file_contents = ""
            while True: # continue always
                line_bytes = ser.readline() # read the line, with \n denoting new line (note, MUST get a \n)
                
                if not capturing and line_bytes: # dont display everything we're getting but show that we are getting something
                    capturing = True
                    print('\nCapturing...\n')

                encoded_line = line_bytes.rstrip() 
                decoded = decrypt_data(encoded_line, key)

                if decoded: #if we have a payload
                    if decoded == "*BEGIN*":
                        file_contents = ""
                    elif decoded == "*END*":
                        with open(output, 'w') as output_lla:
                            output_lla.writelines(file_contents)
                            output_lla.close()
                    else:
                        file_contents+=decoded
                    
    except serial.SerialException as e:
        print(f"Error accessing the port: {e}")

    except KeyboardInterrupt:
        print("\nExiting script.")

    finally:
        # ensure the port is always closed gracefully
        if ser.isOpen():
            ser.close()
            print("Port closed.")

if __name__ == '__main__':
    config = ConfigParser()
    config.read('host_config.ini')
    capture()