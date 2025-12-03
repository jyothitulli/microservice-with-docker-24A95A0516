#!/usr/bin/env python3

import os
import time
from datetime import datetime, timezone
import pyotp
import binascii

SEED_PATH = "/app/data/seed.txt"
OUTPUT = "/app/cron/last_code.txt"


def read_seed():
    try:
        with open(SEED_PATH, "r") as f:
            seed_hex = f.read().strip()
        seed_bytes = binascii.unhexlify(seed_hex)
        seed_base32 = pyotp.utils.base32.b32encode(seed_bytes).decode()
        return seed_base32
    except Exception as e:
        return None


def log_totp():
    seed_base32 = read_seed()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if seed_base32:
        totp = pyotp.TOTP(seed_base32)
        code = totp.now()
        log = f"{timestamp} - 2FA Code: {code}"
    else:
        log = f"{timestamp} - ERROR: Seed not found"

    print(log)


if __name__ == "__main__":
    log_totp()
