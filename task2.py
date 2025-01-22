from Crypto.Random import get_random_bytes
import urllib.parse
import task1


def main():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    # Submit function takes in a string and returns a string with added data
    # take an arbitrary string provided by the user, and prepend the string: "userid=456; userdata="
    # and append the string: ";session-id=31337"
    # Also:
    # (1) URL encode any ‘;’ and ‘=’ characters that appear in the user provided string;
    # (2) pad the final string(using PKCS # 7), and
    # (3) encrypt the padded string using the AES - 128 - CBC you implemented in Task  1
    def submit(input_txt):
        encoded_txt = urllib.parse.quote(input_txt)
        print(type(encoded_txt))
        print(encoded_txt)
        padded_txt = pad(bytes(encoded_txt, "utf-8"))
        print(padded_txt)
        encrypted = task1.cbc_encrypt(padded_txt, key, iv)
        return encrypted

    # takes plaintext (string) and adds padding using PKCS#7 method
    def pad(message):
        padding_length = 16 - (len(message) % 16)
        padding = bytes([padding_length] * padding_length)
        return message + padding

    submit("You’re the man; now=dog")

if __name__ == '__main__':
    main()