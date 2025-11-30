import hashlib

SEPARATOR = ":::"

def hash_message(ciphertext):
    """Return SHA-256 hex digest of encrypted message."""
    return hashlib.sha256(ciphertext.encode("utf-8")).hexdigest()

def attach_hash(ciphertext):
    """Append the SHA-256 hash to the ciphertext using SEPARATOR."""
    digest = hash_message(ciphertext)
    return f"{ciphertext}{SEPARATOR}{digest}"

def split_message_and_hash(stego_output):
    """Separate the encrypted message and its stored hash."""
    if SEPARATOR not in stego_output:
        raise ValueError("Integrity data missing from message.")
    ciphertext, stored_hash = stego_output.split(SEPARATOR, 1)
    return ciphertext, stored_hash

def verify_hash(ciphertext, stored_hash):
    """Check whether the SHA-256 hash matches."""
    calculated_hash = hash_message(ciphertext)
    return calculated_hash == stored_hash
