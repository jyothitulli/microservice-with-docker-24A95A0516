# app/cron_generate_2fa.py
from datetime import datetime
import os
from app.totp_utils import generate_totp_code

SEED_PATH = "/data/seed.txt"
OUTPUT_PATH = "/cron/2fa.log"

# Check if seed exists
if not os.path.exists(SEED_PATH):
    with open(OUTPUT_PATH, "a") as f:
        f.write("No seed available\n")
    exit(1)

# Read seed
with open(SEED_PATH) as f:
    hex_seed = f.read().strip()

# Generate OTP
code = generate_totp_code(hex_seed)

# Timestamp
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Write to cron log
with open(OUTPUT_PATH, "a") as f:
    f.write(f"{timestamp} - 2FA Code: {code}\n")
