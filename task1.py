#Image Reading and Preparation:
#   Function to read BMP header
#   Open image file and separate header from image data

#Key and IV Generation:
#   Generate random key
#   Generate random IV (for CBC mode)

# Padding:
#   PKCS#7 padding function

# Encryption: a) ECB mode:
#   Function for ECB encryption b) CBC mode:
#   Function for CBC encryption

# Decryption:
#     ECB decryption function
#     CBC decryption function

# Visualization:
#    Function to display original, ECB-encrypted, and CBC-encrypted images side by side

# Main Process:
#   Load image
#   Generate key and IV
#   Encrypt using ECB and CBC
#   Decrypt ECB and CBC encrypted images
#   Display results

#Image Reading and Preparation:
#   Function to read BMP header
#   Open image file and separate header from image data

#Key and IV Generation:
#   Generate random key
#   Generate random IV (for CBC mode)

# Padding:
#   PKCS#7 padding function

# Encryption: a) ECB mode:
#   Function for ECB encryption b) CBC mode:
#   Function for CBC encryption

# Decryption:
#     ECB decryption function
#     CBC decryption function

# Visualization:
#    Function to display original, ECB-encrypted, and CBC-encrypted images side by side

# Main Process:
#   Load image
#   Generate key and IV
#   Encrypt using ECB and CBC
#   Decrypt ECB and CBC encrypted images
#   Display results

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def main():

    # encrypt_image takes a file (string), mode (string), and potentially keys (strings) and creates an encrypted file using the given mode and key
    def encrypt_image(img_filename, mode, key=None, iv=None):
        with open(img_filename, 'rb') as file:
            header = file.read(54)
            plaintext = file.read()[len(header):] #read rest of the image data

        # padding
        bits = len(plaintext)
        remainder = bits % 128
        for i in range(remainder):
            plaintext.append(hex(remainder))

        # following block given by Prof.
        # Encrypt based on mode
        if key is None:
            key = get_random_bytes(16)

        if mode == 'ECB':
            ciphertext = ecb_encrypt(plaintext, key)
            data = header + ciphertext
        else: #mode is CBC
            if iv is None:
                iv = get_random_bytes(16)
            ciphertext = cbc_encrypt(plaintext, key, iv)
            data = header + iv + ciphertext

    def ecb_encrypt(plaintext, key):
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher

    def cbc_encrypt(plaintext, key, iv):
        return AES.new(key, AES.MODE_ECB)

    encrypt_image('cp-logo.bmp', 'ECB')

if __name__ == "__main__":
    main()