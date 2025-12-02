import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP
    """
    encrypted_data = base64.b64decode(encrypted_seed_b64)

    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed_str = decrypted.decode("utf-8").strip()

    # Validation: must be 64-char hex string
    if len(seed_str) != 64 or not all(c in "0123456789abcdef" for c in seed_str.lower()):
        raise ValueError("Invalid seed format! Expected 64-character hex.")

    return seed_str


def load_private_key(filename="student_private.pem"):
    with open(filename, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )


def main():
    private_key = load_private_key()

    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed = f.read().strip()

    try:
        seed = decrypt_seed(encrypted_seed, private_key)
        print("Decrypted Seed:", seed)

        # Save to file (will later be copied into Docker image)
        with open("seed.txt", "w") as seed_file:
            seed_file.write(seed)

        print("Seed saved to seed.txt successfully!")
    except Exception as e:
        print("Decryption failed:", str(e))


if __name__ == "__main__":
    main()
