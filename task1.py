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

def main():

    # encrypt_image takes a file (string), mode (string), and potentially keys (strings) and creates an encrypted file using the given mode and key
    def encrypt_image(img_filename, mode, key=None, iv=None):
        with open(img_filename, 'rb') as file:
            header = file.read(138) #read the first 138 bytes
            header = header[:54]
            plaintext = img_filename.read()[len(header):]#read rest of the image data


        # following block given by Prof. Yocam
        # Encrypt based on mode
        if mode == 'ECB':
            if key is None:
                key = AES.new(key, AES.MODE_ECB)
            ciphertext = ecb_encrypt(plaintext, key)
            data = header + ciphertext
        else:
            ciphertext = cbc_encrypt(plaintext, key, iv)
            data = header + iv + ciphertext


if __name__ == "__main__":
    main()