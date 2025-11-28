"""
Randomized Invisible Character Mapping Module

This module generates password-derived character mappings for text steganography.
It provides deterministic, reproducible mappings based on the user's password,
making hidden messages harder to detect through statistical analysis.

Author: Text Steganography Team
Feature: Randomized Invisible Character Mapping
"""

import hashlib
import random
from Crypto.Protocol.KDF import PBKDF2


# Expanded pool of invisible Unicode characters (16 total)
# These characters are invisible in most text renderers but have distinct Unicode values
INVISIBLE_CHAR_POOL = [
    '\u200B',  # Zero Width Space
    '\u200C',  # Zero Width Non-Joiner
    '\u200D',  # Zero Width Joiner
    '\u200E',  # Left-to-Right Mark
    '\u200F',  # Right-to-Left Mark
    '\u202A',  # Left-to-Right Embedding
    '\u202B',  # Right-to-Left Embedding
    '\u202C',  # Pop Directional Formatting
    '\u202D',  # Left-to-Right Override
    '\u202E',  # Right-to-Left Override
    '\u2060',  # Word Joiner
    '\u2061',  # Function Application
    '\u2062',  # Invisible Times
    '\u2063',  # Invisible Separator
    '\u2064',  # Invisible Plus
    '\uFEFF',  # Zero Width No-Break Space
]


def derive_mapping_seed(password):
    """
    Derives a deterministic seed from the password using PBKDF2.
    Uses the same salt as AES encryption for consistency, but different bytes
    to avoid correlation with the encryption key.

    Args:
        password (str): User's password

    Returns:
        int: Deterministic seed value derived from password
    """
    salt = b"this is a salt"  # Same salt as AES.py:7 for consistency
    kdf = PBKDF2(password, salt, 64, 1000)

    # Use bytes 32-40 for mapping seed (AES uses bytes 0-32 for encryption key)
    # This ensures the mapping seed is independent from the encryption key
    seed_bytes = kdf[32:40]
    seed = int.from_bytes(seed_bytes, byteorder='big')

    return seed


def generate_mapping(password):
    """
    Generates deterministic ZWC and ZWC_reverse mappings from password.
    Same password always produces the same mapping, ensuring sender and receiver
    can synchronize without transmitting the mapping itself.

    The function:
    1. Derives a seed from the password using PBKDF2
    2. Uses the seed to randomly select 4 characters from the pool
    3. Creates bidirectional mapping dictionaries

    Args:
        password (str): User's password

    Returns:
        tuple: (ZWC dict, ZWC_reverse dict)
            - ZWC: Maps 2-bit binary strings to invisible Unicode characters
            - ZWC_reverse: Maps invisible Unicode characters back to 2-bit binary

    Example:
        >>> ZWC, ZWC_reverse = generate_mapping("mypassword123")
        >>> ZWC["00"]
        '\u2060'
        >>> ZWC_reverse['\u2060']
        '00'
    """
    # Derive deterministic seed from password
    seed = derive_mapping_seed(password)
    random.seed(seed)

    # Randomly select 4 unique characters from the pool
    # This provides C(16,4) × 4! = 43,680 possible mappings
    selected_chars = random.sample(INVISIBLE_CHAR_POOL, 4)

    # Create forward mapping: binary pairs -> invisible characters
    ZWC = {
        "00": selected_chars[0],
        "01": selected_chars[1],
        "10": selected_chars[2],
        "11": selected_chars[3],
    }

    # Create reverse mapping: invisible characters -> binary pairs
    ZWC_reverse = {v: k for k, v in ZWC.items()}

    return ZWC, ZWC_reverse


def get_mapping_hash(ZWC):
    """
    Creates a hash of the current mapping for verification and debugging.
    This hash can be used to confirm that sender and receiver are using
    the same character mapping without revealing the mapping itself.

    Args:
        ZWC (dict): Character mapping dictionary

    Returns:
        str: 8-character hexadecimal hash of the mapping

    Example:
        >>> ZWC, _ = generate_mapping("test123")
        >>> hash_val = get_mapping_hash(ZWC)
        >>> len(hash_val)
        8
    """
    # Concatenate all characters in sorted key order for consistency
    mapping_str = "".join([ZWC[k] for k in sorted(ZWC.keys())])

    # Hash using SHA-256 and return first 8 characters
    hash_digest = hashlib.sha256(mapping_str.encode('utf-16')).hexdigest()
    return hash_digest[:8]


# Testing and verification functions
if __name__ == "__main__":
    # Determinism test: same password should always produce same mapping
    print("Testing determinism...")
    ZWC1, ZWC_rev1 = generate_mapping("password123")
    ZWC2, ZWC_rev2 = generate_mapping("password123")
    assert ZWC1 == ZWC2, "FAIL: Same password produced different mappings"
    print("✓ Determinism test passed")

    # Uniqueness test: different passwords should produce different mappings
    print("\nTesting uniqueness...")
    ZWC_a, _ = generate_mapping("passwordA")
    ZWC_b, _ = generate_mapping("passwordB")
    assert ZWC_a != ZWC_b, "FAIL: Different passwords produced same mapping"
    print("✓ Uniqueness test passed")

    # Character pool validation
    print("\nTesting character pool...")
    ZWC, ZWC_rev = generate_mapping("test")
    for bit_pair, char in ZWC.items():
        assert char in INVISIBLE_CHAR_POOL, f"FAIL: Character {repr(char)} not in pool"
    print("✓ Character pool test passed")

    # Reversibility test
    print("\nTesting reversibility...")
    for bit_pair, char in ZWC.items():
        assert ZWC_rev[char] == bit_pair, "FAIL: Reverse mapping doesn't match"
    print("✓ Reversibility test passed")

    # Display example mapping
    print("\n" + "="*60)
    print("Example mapping for password 'demo123':")
    print("="*60)
    ZWC_demo, _ = generate_mapping("demo123")
    hash_demo = get_mapping_hash(ZWC_demo)
    print(f"Mapping hash: {hash_demo}")
    for bit_pair in sorted(ZWC_demo.keys()):
        char = ZWC_demo[bit_pair]
        print(f"  '{bit_pair}' -> U+{ord(char):04X} ({char!r})")

    print("\n✓ All tests passed successfully!")
