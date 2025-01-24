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
    slash_pos = full_msg.index('/') # Find position of '/'

    msg_bytes = full_msg.encode("utf-8") #turn msg into bytes
    padded_txt = pad(msg_bytes) # encode to turn full_msg into bytes

    print("plaintext before encryption", padded_txt)
    encrypted = task1.cbc_encrypt(padded_txt, key, iv)
    print("Encrypted text", encrypted)
    return encrypted, slash_pos

# Verify takes
def verify(encrypted_input):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_input) #decrypt input using AES library
    print("Decrypted input:", decrypted)
    return "admin=true" in decrypted

# performs a bit flip attack making verify return true
def attack(message, slash_pos):
    # Show ciphertext before the flip
    print("\nBefore admin/true - Ciphertext (hex):")
    ciphertext_hex = ''.join([hex(x)[2:].zfill(2) for x in message])
    print(ciphertext_hex)

    # Calculate which block needs modification
    block_num = (slash_pos // 16) # Block containing the target byte
    pos_in_prev_block = slash_pos % 16
    prev_block_start = (block_num - 1) * 16 # Start of previous block

    # XOR the byte in previous block
    modified_ciphertext = bytearray(message)
    modified_ciphertext[prev_block_start + pos_in_prev_block] ^= (ord('/') ^ ord('='))

    # Show ciphertext after the flip
    print("\nAfter admin=true - Ciphertext (hex):")
    modified_hex = ''.join([hex(x)[2:].zfill(2) for x in modified_ciphertext])
    print(modified_hex)

    # Show the changed byte
    print(f"\nChanged byte position: {prev_block_start + pos_in_prev_block}")
    print(f"Original byte: {hex(message[prev_block_start + pos_in_prev_block])[2:].zfill(2)}")
    print(f"Modified byte: {hex(modified_ciphertext[prev_block_start + pos_in_prev_block])[2:].zfill(2)}")

    # Decrypt modified ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(modified_ciphertext)
    print(f"\nPlaintext after byte-flip:", decrypted)
    return modified_ciphertext

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
    sub, pos = submit("admin/true")
    print(attack(sub, pos))
    # print(verify(sub))
    # print(verify(attack(b'userid=456;userdata=admin/true;session-id=31337')))
