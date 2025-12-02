from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from app.crypto_utils import hex_to_base32, generate_totp_code, verify_totp_code
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

DATA_PATH = Path("data/seed.txt")
PRIVATE_KEY_PATH = Path("data/private_key.pem")  # your private key file

app = FastAPI(title="TOTP Authentication API")


# ---------- Request Models ----------
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str


class Verify2FARequest(BaseModel):
    code: str


# ---------- Endpoint 1: Decrypt Seed ----------
@app.post("/decrypt-seed")
def decrypt_seed(request: DecryptSeedRequest):
    try:
        if not PRIVATE_KEY_PATH.exists():
            raise HTTPException(status_code=500, detail="Private key not found")

        # Load private key
        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = RSA.import_key(f.read())
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=None)  # SHA-256 is default in PyCryptodome

        # Decode and decrypt
        encrypted_bytes = base64.b64decode(request.encrypted_seed)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        hex_seed = decrypted_bytes.decode("utf-8")

        # Validate 64-character hex
        if len(hex_seed) != 64 or not all(c in "0123456789abcdefABCDEF" for c in hex_seed):
            raise HTTPException(status_code=500, detail="Invalid decrypted seed")

        # Save to seed.txt
        DATA_PATH.parent.mkdir(exist_ok=True)
        with open(DATA_PATH, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")


# ---------- Endpoint 2: Generate 2FA ----------
@app.get("/generate-2fa")
def generate_2fa():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = DATA_PATH.read_text().strip()
    code, remaining = generate_totp_code(hex_seed)
    return {"code": code, "valid_for": remaining}


# ---------- Endpoint 3: Verify 2FA ----------
@app.post("/verify-2fa")
def verify_2fa(request: Verify2FARequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="Missing code")
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = DATA_PATH.read_text().strip()
    is_valid = verify_totp_code(hex_seed, request.code)
    return {"valid": is_valid}
