from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from urllib.parse import quote, unquote
import task1

key = get_random_bytes(16)
iv = get_random_bytes(16)

# Submit function takes in a string and returns an encoded string with added data
def submit(input_txt):
    input_txt = quote(input_txt) #url encode
    full_msg = f"userid=456;userdata={input_txt};session-id=31337"
    msg_bytes = full_msg.encode("utf-8") #turn msg into bytes
    padded_txt = pad(msg_bytes) # encode to turn full_msg into bytes
    print("plaintext before encryption", padded_txt)
    encrypted = task1.cbc_encrypt(padded_txt, key, iv)
    return encrypted

# Verify takes
def verify(encrypted_input):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_input) #decrypt input using AES library
    decrypted = unpad(decrypted).decode("utf-8") #unpad it and decode into a string
    return ";admin=true" in decrypted

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
    sub = submit("You're the man; now=dog")
    print(verify(sub))