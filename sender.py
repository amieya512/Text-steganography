from embed import embedFunc
from AES import encrypt
import pyperclip as py

from sanitizer import sanitize_cover_text
from enhancements.integrity import attach_hash


def hideFunc(SM, password, CM):
    """
    Encrypts a secret message, attaches an integrity hash,
    and embeds it into a sanitized cover text.
    """

    # Sanitize cover text
    CM, removed = sanitize_cover_text(CM)

    # Encrypt message
    encSM = encrypt(password, SM)

    # Attach hash for integrity checking
    encSM_with_hash = attach_hash(encSM)

    # Embed encrypted message + hash into cover text
    CM_HM = embedFunc(encSM_with_hash, CM)

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
