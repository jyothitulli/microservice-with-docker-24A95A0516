#!/usr/bin/env python3
import datetime
import pyotp
import os
import base64  # <-- add this

def load_hex_seed():
    try:
        with open("/data/seed.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

hex_seed = load_hex_seed()
if not hex_seed:
    print("No seed available")
    exit()

# Convert hex → base32
seed_bytes = bytes.fromhex(hex_seed)
base32_seed = base64.b32encode(seed_bytes).decode('utf-8')  # <-- fixed line

totp = pyotp.TOTP(base32_seed)
code = totp.now()

timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

print(f"{timestamp} - 2FA Code: {code}")
