from embed import embedFunc
from AES import encrypt
from randomized_mapping import generate_mapping, get_mapping_hash
import pyperclip as py

from sanitizer import sanitize_cover_text
from enhancements.integrity import attach_hash


def hideFunc(SM, password, CM):
    """
    Encrypts a secret message, attaches an integrity hash,
    and embeds it into a sanitized cover text using randomized character mapping.

    Combines three security features:
    1. Randomized character mapping (password-derived)
    2. SHA-256 integrity verification
    3. Cover text sanitization
    """

    # Feature 3: Sanitize cover text (teammate's feature)
    CM, removed = sanitize_cover_text(CM)

    # Encrypt message with AES
    encSM = encrypt(password, SM)

    # Feature 2: Attach hash for integrity checking (teammate's feature)
    encSM_with_hash = attach_hash(encSM)

    # Feature 1: Generate password-derived randomized character mapping (your feature)
    ZWC, ZWC_reverse = generate_mapping(password)

    # Optional: Print mapping hash for debugging and verification
    mapping_hash = get_mapping_hash(ZWC)
    print(f"Using character mapping (hash: {mapping_hash})")

    print("Encrypted secret message going to send:", encSM_with_hash)

    # Embed encrypted message + hash into cover text using randomized mapping
    CM_HM = embedFunc(encSM_with_hash, CM, ZWC, ZWC_reverse)

    print("Cover message=", CM_HM)

    # Copy to clipboard
    py.copy(CM_HM)

    # Save output for debugging
    with open("stego.txt", "w", encoding="utf-8") as f:
        f.write(CM_HM)

    return CM_HM


if __name__ == "__main__":
    print("=== AITSteg Text Steganography ===\n")
    SM = input("Enter secret message to hide: ").strip()
    CM = input("Enter cover message (normal text): ").strip()
    password = input("Enter password for AES encryption: ").strip()

    try:
        hideFunc(SM, password, CM)
        print("\nStego message saved to stego.txt")
    except Exception as e:
        print(f"\nError: {e}")
