# from app.crypto_utils import generate_totp_code, verify_totp_code

# # Load decrypted seed
# with open("data/seed.txt", "r") as f:
#     hex_seed = f.read().strip()

# # Generate TOTP
# code, remaining = generate_totp_code(hex_seed)
# print(f"TOTP Code: {code}, valid for next {remaining} seconds")

# # Verify TOTP
# user_input = input("Enter the TOTP code: ")
# if verify_totp_code(hex_seed, user_input):
#     print("✅ Verified!")
# else:
#     print("❌ Invalid code")
from fastapi import FastAPI, HTTPException
import os
from app.crypto_utils import generate_totp_code, verify_totp_code

app = FastAPI()

SEED_FILE = "/data/seed.txt"

def read_seed():
    if not os.path.exists(SEED_FILE):
        raise FileNotFoundError("Seed file missing!")
    with open(SEED_FILE, 'r') as f:
        return f.read().strip()

@app.get("/")
def home():
    return {"message": "Auth Service Running!"}

@app.get("/generate")
def generate_code():
    seed = read_seed()
    code = generate_totp(seed)
    return {"totp_code": code}

@app.post("/verify/{code}")
def verify_code(code: str):
    seed = read_seed()
    is_valid = verify_totp(seed, code)
    if is_valid:
        return {"status": "Valid Code"}
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired code")
