import sys
sys.path

from embed import embedFunc
from extract import extractFunc
from AES import encrypt, decrypt
import pyperclip as py
from enhancements.integrity import attach_hash


def hideFunc(SM, password, CM):
    # Encrypt using AES
    encSM = encrypt(password, SM)
    print("Encrypted secret message going to send:", encSM)

    # Attach the SHA-256 hash
    encSM_with_hash = attach_hash(encSM)

    # Embed ciphertext + hash
    CM_HM = embedFunc(encSM_with_hash, CM)

    print("Cover message=", CM_HM)

    # Copy to clipboard
    py.copy(CM_HM)

    # Save stego message to file so we don't need to copy manually
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
        print("\nThe stego message has also been saved to stego.txt")
    except Exception as e:
        print(f"\nError: {e}")
