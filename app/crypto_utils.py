import base64
from binascii import unhexlify
import pyotp
import time


def hex_to_base32(hex_seed: str) -> str:
    """
    Converts a 64-character hexadecimal seed string to Base32 encoding.
    """
    if len(hex_seed) != 64:
        raise ValueError("Hex seed must be exactly 64 characters long.")

    try:
        hex_bytes = unhexlify(hex_seed)  # Convert hex to bytes
        base32_encoded = base64.b32encode(hex_bytes).decode('utf-8')
        return base32_encoded.rstrip('=')  # Remove padding for clean key
    except Exception as e:
        raise ValueError(f"Failed to convert hex seed to Base32: {e}")

def generate_totp_code(hex_seed: str) -> tuple[str, int]:
    """
    Generates the current TOTP code and the remaining seconds in the period.
    Returns: (code_string, remaining_seconds)
    """
    base32_seed = hex_to_base32(hex_seed)  # Convert hex to Base32
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)
    code = totp.now()  # Generate 6-digit TOTP code
    remaining = 30 - (int(time.time()) % 30)  # Time left in current window
    return code, remaining

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verifies a TOTP code with time window tolerance.
    Returns True if valid, False otherwise.
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6)
    return totp.verify(code, valid_window=valid_window)