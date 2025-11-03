import sys
from embed import embedFunc
from extract import extractFunc
from AES import encrypt, decrypt
import pyperclip as py


def hideFunc(SM, password, CM):
    encSM = encrypt(password, SM)
    print("Encrypted secret message going to send:", encSM)
    CM_HM = embedFunc(encSM, CM)
    print("\nCover message =", CM_HM)
    py.copy(CM_HM)
    print("\n✅ The stego message has been copied to your clipboard.")
    return CM_HM


if __name__ == "__main__":
    print("=== AITSteg Text Steganography ===\n")
    SM = input("Enter secret message to hide: ").strip()
    CM = input("Enter cover message (normal text): ").strip()
    password = input("Enter password for AES encryption: ").strip()

    try:
        hideFunc(SM, password, CM)
        print("\nDone! You can now paste the hidden text wherever you like.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


