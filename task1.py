from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# encrypt_image takes a file (string), mode (string), and potentially keys (strings) and creates an encrypted file using the given mode, and key
# Returns nothing but outputs an encrypted bmp file
def encrypt_image(img_filename, mode, key=None, iv=None):
    with open(img_filename, 'rb') as file:
        header = file.read(54)
        plaintext = file.read() #read rest of the image data

    #add padding
    padded_plaintext = pad(plaintext)

    # following block given by Prof.
    # Encrypt based on mode
    if key is None:
        key = get_random_bytes(16)

    if mode == 'ECB':
        output = header + ecb_encrypt(padded_plaintext, key)
    elif mode == 'CBC':
        if iv is None:
            iv = get_random_bytes(16)
        output = header + cbc_encrypt(padded_plaintext, key, iv)
    else:
        raise NotImplementedError("Mode not implemented")

    # write encrypted date to file
    with open(f"{img_filename.replace('.bmp', '')}_{mode}_encrypted.bmp", "wb") as file:
        file.write(output)

    print("encrypted image", img_filename, "in mode", mode)

# takes plaintext (string) and adds padding using PKCS#7 method
def pad(plaintext):
    padding_size = 16 - (len(plaintext) % 16) #compute # padding bytes
    padding = bytes([padding_size] * padding_size) # creates padding_size bytes of value padding_size
    return plaintext + padding

# takes plaintext (bytes), a cipher, and ciphertext (bytes) and returns plaintext encrypted in ECB mode
def ecb_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)  # user MODE_ECB for both because MODE_CBC automatically xors it
    ciphertext = bytes(0)
    for i in range(0, len(plaintext), 16):
        ciphertext += cipher.encrypt(plaintext[i:i + 16]) #encrypt one block
    return ciphertext

# takes plaintext (bytes), an iv, a cipher, and ciphertext (bytes) and returns plaintext encrypted in CBC mode
def cbc_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)  # user MODE_ECB for both because MODE_CBC automatically xors it
    ciphertext = bytes(0)
    prev_block = iv
    for i in range(16, len(plaintext), 16):
        block = plaintext[i:i + 16]
        xor_block = bytes(a ^ b for a, b in zip(block, prev_block)) #xor bytes to prev_block
        ciphertext += cipher.encrypt(xor_block)
        prev_block = xor_block
    return ciphertext

if __name__ == '__main__':
    #test
    encrypt_image('cp-logo.bmp', 'ECB')
