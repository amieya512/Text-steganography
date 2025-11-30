from extract import extractFunc
from AES import decrypt
from randomized_mapping import generate_mapping, get_mapping_hash

# New imports for integrity checking
from enhancements.integrity import split_message_and_hash, verify_hash


def revealFunc(CM_HM, password):
    """
    Extracts and decrypts a hidden message with integrity verification
    using randomized character mapping.

    Combines three security features:
    1. Randomized character mapping (password-derived)
    2. SHA-256 integrity verification
    3. Cover text sanitization
    """

    # Feature 1: Regenerate same password-derived mapping used by sender (your feature)
    ZWC, ZWC_reverse = generate_mapping(password)

    # Optional: Print mapping hash for debugging and verification
    mapping_hash = get_mapping_hash(ZWC)
    print(f"Using character mapping (hash: {mapping_hash})")

    # Extract the raw content (ciphertext + hash) using randomized mapping
    SM_extract = extractFunc(CM_HM, ZWC_reverse)

    try:
        # Feature 2: Separate encrypted message from stored hash (teammate's feature)
        ciphertext, stored_hash = split_message_and_hash(SM_extract)
    except ValueError as e:
        # Integrity data missing or malformed
        msg = f"Integrity Error: {e}"
        print(msg)
        return msg

    # Verify that the SHA-256 hash matches
    if not verify_hash(ciphertext, stored_hash):
        msg = "Integrity check failed: hidden message was modified or corrupted."
        print(msg)
        return msg

    # If valid, decrypt the encrypted portion
    plaintext = decrypt(password, ciphertext)
    print("Your secret message:", plaintext)
    return plaintext
