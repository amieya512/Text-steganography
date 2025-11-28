from extract import extractFunc
from AES import decrypt
from randomized_mapping import generate_mapping, get_mapping_hash

# CM_HM=input("Enter cover message:")
# password=input("Enter password:")

def revealFunc(CM_HM, password):
    # Regenerate same password-derived mapping used by sender
    ZWC, ZWC_reverse = generate_mapping(password)

    # Optional: Print mapping hash for debugging and verification
    mapping_hash = get_mapping_hash(ZWC)
    print(f"Using character mapping (hash: {mapping_hash})")

    # Extract using same randomized mapping
    SM_extract = extractFunc(CM_HM, ZWC_reverse)
    print("Your secret message:", decrypt(password, SM_extract))
    return decrypt(password, SM_extract)
