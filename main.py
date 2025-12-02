from app.crypto_utils import generate_totp_code, verify_totp_code

# Load decrypted seed
with open("data/seed.txt", "r") as f:
    hex_seed = f.read().strip()

# Generate TOTP
code, remaining = generate_totp_code(hex_seed)
print(f"TOTP Code: {code}, valid for next {remaining} seconds")

# Verify TOTP
user_input = input("Enter the TOTP code: ")
if verify_totp_code(hex_seed, user_input):
    print("✅ Verified!")
else:
    print("❌ Invalid code")
