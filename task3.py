import matplotlib.pyplot as plt
import subprocess

# Run OpenSSL speed test for RSA
cmd = ["openssl", "speed", "rsa"]
result = subprocess.run(cmd, capture_output=True, text=True)

# Print raw output
print(result.stdout)
