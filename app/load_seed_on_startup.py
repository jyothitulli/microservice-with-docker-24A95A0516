import os
from app.crypto_utils import decrypt_seed

SEED_PATH = "/data/seed.txt"
ENCRYPTED_SEED_ENV = "ENCRYPTED_SEED"

def ensure_seed():
    os.makedirs(os.path.dirname(SEED_PATH), exist_ok=True)
    if os.path.exists(SEED_PATH):
        return

    # Try to read seed from environment variable for container startup
    encrypted_seed = os.environ.get(ENCRYPTED_SEED_ENV)
    if encrypted_seed:
        hex_seed = decrypt_seed(encrypted_seed)
        with open(SEED_PATH, "w") as f:
            f.write(hex_seed + "\n")
        print("Seed initialized at container startup")
    else:
        print("No encrypted seed found, skipping seed initialization")
