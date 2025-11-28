import sys
sys.path

from embed import embedFunc
from extract import extractFunc
from AES import encrypt, decrypt
from randomized_mapping import generate_mapping, get_mapping_hash
import pyperclip as py

# SM=input("Enter secret message:")
# CM=input("Enter cover message:")
# password=input("Enter password for encryption:")

def hideFunc(SM, password, CM):
    # Generate password-derived randomized character mapping
    ZWC, ZWC_reverse = generate_mapping(password)

    # Optional: Print mapping hash for debugging and verification
    mapping_hash = get_mapping_hash(ZWC)
    print(f"Using character mapping (hash: {mapping_hash})")

    # Encrypt secret message using AES
    encSM = encrypt(password, SM)
    print("Encrypted secret message going to send:", encSM)

    # Embed using randomized mapping
    CM_HM = embedFunc(encSM, CM, ZWC, ZWC_reverse)
    print("Cover message=", CM_HM)
    py.copy(CM_HM)
    return CM_HM
    

#print("copy this message and paste it to send")


