from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(message):
    padding_length = 16 - (len(message) % 16)
    padding = bytes([padding_length] * padding_length)
    return message + padding

# Original message
def main():
    message = b'userid=456;userdata=admin/true;session-id=31337'
    print(f"Plaintext before byte-flip: {message.decode('ascii')}")

    # Generate key and IV
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    # Find position of '/'
    slash_pos = message.index(b'/')

    # Encrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message)
    ciphertext = cipher.encrypt(padded_message)

    # Show ciphertext before the flip
    print("\nBefore admin/true - Ciphertext (hex):")
    ciphertext_hex = ''.join([hex(x)[2:].zfill(2) for x in ciphertext])
    print(ciphertext_hex)

    # Calculate which block needs modification
    block_num = (slash_pos // 16) # Block containing the target byte
    pos_in_prev_block = slash_pos % 16
    prev_block_start = (block_num - 1) * 16 # Start of previous block

    # XOR the byte in previous block
    modified_ciphertext = bytearray(ciphertext)
    modified_ciphertext[prev_block_start + pos_in_prev_block] ^= (ord('/') ^ ord('='))

    # Show ciphertext after the flip
    print("\nAfter admin=true - Ciphertext (hex):")
    modified_hex = ''.join([hex(x)[2:].zfill(2) for x in modified_ciphertext])
    print(modified_hex)

    # Show the changed byte
    print(f"\nChanged byte position: {prev_block_start + pos_in_prev_block}")
    print(f"Original byte: {hex(ciphertext[prev_block_start + pos_in_prev_block])[2:].zfill(2)}")
    print(f"Modified byte: {hex(modified_ciphertext[prev_block_start + pos_in_prev_block])[2:].zfill(2)}")

    # Decrypt modified ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(modified_ciphertext)
    print(f"\nPlaintext after byte-flip:", decrypted)


if __name__ == "__main__":
    main()
# Plaintext before byte-flip: userid=456;userdata=admin/true;session-id=31337
# Before admin/true - Ciphertext (hex):
# 9511f51e9a6069323cde133ef6eb20a4adc7ed26ae11a7f6acc3544e0689de1f970ec51684a5c71f6b77c6428748cccf
# After admin=true - Ciphertext (hex):
# 9511f51e9a6069323ccc133ef6eb20a4adc7ed26ae11a7f6acc3544e0689de1f970ec51684a5c71f6b77c6428748cccf
# Changed byte position: 9
# Original byte: de
# Modified byte: cc
# Plaintext after byte-flip: userid=456;userdata=admin=true;session-id=31337

# modify that doesn't work
# takes output from submit and alters it so verify returns true
# def modify(ciphertext, message):
#     message_bytes = message.encode("utf-8")
#     if b'/' not in message_bytes:
#         raise ValueError("plaintext must contain '/'")
#     slash_pos = message_bytes.index(b'/')
#
    # #calculate which block / is in
    # block_num = (slash_pos // 16)
    # pos_in_prev_block = slash_pos % 16
    # prev_block_start = (block_num - 1) * 16
    #
    # # modify byte
    # modified_ciphertext = bytearray(ciphertext)
    # modified_ciphertext[prev_block_start+pos_in_prev_block] ^= (ord('/') ^ ord('='))
#
#     print("modified_ciphertext", modified_ciphertext)
#     return verify(modified_ciphertext)