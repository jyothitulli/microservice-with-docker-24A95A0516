#!/usr/bin/env python3

import subprocess
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


# --------------------------------------------------
# Load commit hash
# --------------------------------------------------
def get_commit_hash():
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H"],
        capture_output=True,
        text=True
    )
    commit_hash = result.stdout.strip()
    if len(commit_hash) != 40:
        raise ValueError("Invalid commit hash length")
    return commit_hash


# --------------------------------------------------
# Sign commit hash using RSA-PSS with SHA256
# --------------------------------------------------
def sign_message(message: str, private_key):
    signature = private_key.sign(
        message.encode("utf-8"),   # IMPORTANT: ASCII string
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256()
    )
    return signature


# --------------------------------------------------
# Encrypt signature using RSA/OAEP-SHA256
# --------------------------------------------------
def encrypt_with_public_key(data: bytes, public_key):
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def main():
    # Step 1: Commit Hash
    commit_hash = get_commit_hash()
    print(f"Commit Hash: {commit_hash}")

    # Step 2: Load Student Private Key
    with open("student_private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Step 3: Create Signature
    signature = sign_message(commit_hash, private_key)

    # Step 4: Load Instructor Public Key
    with open("instructor_public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Step 5: Encrypt Signature
    encrypted_signature = encrypt_with_public_key(signature, public_key)

    # Step 6: Base64 Encode
    proof = base64.b64encode(encrypted_signature).decode("utf-8")

    print(f"\nEncrypted Signature (Base64):\n{proof}")


if __name__ == "__main__":
    main()
