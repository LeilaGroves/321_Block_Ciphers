from Crypto.Random import get_random_bytes
import urllib.parse
import task1

key = get_random_bytes(16)
iv = get_random_bytes(16)

# Submit function takes in a string and returns an encoded string with added data
def submit(input_txt):
    encoded_txt = urllib.parse.quote(input_txt)
    full_msg = f"userid=456;userdata={encoded_txt};session-id=31337"
    msg_bytes  = full_msg.encode() #convert message to bytes to add padding
    padded_txt = pad(msg_bytes)
    encrypted = task1.cbc_encrypt(padded_txt, key, iv)
    return encrypted

# takes plaintext (string) and adds padding using PKCS#7 method
def pad(message):
    padding_length = 16 - (len(message) % 16)
    padding = bytes([padding_length] * padding_length)
    return message + padding

submit("You’re the man; now=dog")

if __name__ == '__main__':
    print(submit("You’re the man; now=dog"))