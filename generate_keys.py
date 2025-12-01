from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair(key_size: int = 4096):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )

    # Save private key to PEM file
    with open("student_private.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    public_key = private_key.public_key()

    # Save public key to PEM file
    with open("student_public.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print("RSA 4096-bit keypair generated successfully!")

if __name__ == "__main__":
    generate_rsa_keypair()
