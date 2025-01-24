from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from urllib.parse import quote
import re
import task1

key = get_random_bytes(16)
iv = get_random_bytes(16)

# Submit function takes in a string and returns an encoded string with added data
def submit(input_txt):
    #url encode "=" and ":"
    input_txt = re.sub("=", "%61", input_txt)
    input_txt = re.sub(":", "%58", input_txt)

    full_msg = f"userid=456;userdata={input_txt};session-id=31337"

    msg_bytes = full_msg.encode("utf-8") #turn msg into bytes
    padded_txt = pad(msg_bytes) # encode to turn full_msg into bytes

    print("plaintext before encryption", padded_txt)
    encrypted = task1.cbc_encrypt(padded_txt, key, iv)
    print("Encrypted text", encrypted)
    return encrypted

# Verify takes
def verify(encrypted_input):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_input) #decrypt input using AES library
    decrypted = unpad(decrypted).decode("utf-8") #unpad it and decode into a string
    print("Decrypted input:", decrypted)
    return ";admin=true" in decrypted

# performs a bit flip attack making verify return true
def attack(ciphertext):
    print("Original message", ciphertext)
    ciphertext_hex = ''.join([hex(x)[2:].zfill(2) for x in ciphertext]) #convert to hex
    print("Cipher text hex", ciphertext_hex)

    slash_pos = ciphertext.index(b'/')
    block_num = (slash_pos // 16)
    pos_in_prev_block = slash_pos % 16
    prev_block_start = (block_num - 1) * 16

    modified_ciphertext = bytearray(ciphertext)
    modified_ciphertext[prev_block_start + pos_in_prev_block] ^= (ord('/') ^ ord('='))

    print("Modified ciphertext", modified_ciphertext)
    modified_hex = ''.join([hex(x)[2:].zfill(2) for x in modified_ciphertext])
    print("Modified hex", modified_hex)

    print(f"\nChanged byte position: {prev_block_start + pos_in_prev_block}")
    print(f"Original byte: {hex(ciphertext[prev_block_start + pos_in_prev_block])[2:].zfill(2)}")
    print(f"Modified byte: {hex(modified_ciphertext[prev_block_start + pos_in_prev_block])[2:].zfill(2)}")

# takes message (string) and adds padding using PKCS#7 method
def pad(message):
    padding_length = 16 - (len(message) % 16)
    padding = bytes([padding_length] * padding_length)
    return message + padding

# takes message (strings) and removes padding
def unpad(message):
    padding_length = message[-1]
    return message[:-padding_length]

if __name__ == '__main__':
    sub = submit("admin/true")
    # print(verify(sub))
    print(attack("admin/true"))