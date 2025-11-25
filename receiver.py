from extract import extractFunc
from AES import decrypt

# New imports for integrity checking
from enhancements.integrity import split_message_and_hash, verify_hash


def revealFunc(CM_HM, password):
    # Extract the raw content (ciphertext + hash)
    SM_extract = extractFunc(CM_HM)

    try:
        # Separate encrypted message from stored hash
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
