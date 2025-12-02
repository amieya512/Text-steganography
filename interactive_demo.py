"""
Interactive Text Steganography Demo
Allows users to interactively explore all three security features:
1. Cover Text Sanitization
2. SHA-256 Integrity Verification
3. Randomized Invisible Character Mapping
"""

from sender import hideFunc
from receiver import revealFunc
from randomized_mapping import generate_mapping, get_mapping_hash
from sanitizer import sanitize_cover_text
import sys


def print_header(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80)


def print_subheader(title):
    """Print a formatted subsection header"""
    print(f"\n{title}")
    print("-" * 80)


def show_mapping_details(password):
    """Display the character mapping for a given password"""
    ZWC, _ = generate_mapping(password)
    mapping_hash = get_mapping_hash(ZWC)

    print(f"\nCharacter Mapping (hash: {mapping_hash}):")
    for bit_pair in sorted(ZWC.keys()):
        char = ZWC[bit_pair]
        print(f"  '{bit_pair}' -> U+{ord(char):04X} ({char!r})")
    return mapping_hash


def demo_hide_reveal():
    """Interactive hide and reveal workflow"""
    print_header("HIDE & REVEAL MESSAGE")

    print("\nThis demo will encrypt and hide your secret message inside cover text.")
    print("The same password must be used to reveal it later.")

    # Get inputs
    secret = input("\nEnter your secret message: ").strip()
    if not secret:
        print("❌ Secret message cannot be empty!")
        return

    password = input("Enter password for encryption: ").strip()
    if not password:
        print("❌ Password cannot be empty!")
        return

    cover = input("Enter cover text (normal-looking message): ").strip()
    if not cover or len(cover) < 2:
        print("❌ Cover text must be at least 2 characters!")
        return

    # Show sanitization
    print_subheader("Step 1: Cover Text Sanitization")
    clean_cover, removed = sanitize_cover_text(cover)
    if removed:
        print(f"⚠️  Removed conflicting characters: {removed}")
        print(f"Cleaned cover text: '{clean_cover}'")
    else:
        print("✓ Cover text is clean (no invisible characters to remove)")

    # Show mapping
    print_subheader("Step 2: Password-Derived Character Mapping")
    mapping_hash = show_mapping_details(password)

    # Hide the message
    print_subheader("Step 3: Embedding Secret Message")
    print("Encrypting with AES and embedding with invisible characters...")
    try:
        stego = hideFunc(secret, password, clean_cover)
        print(f"\n✅ Success! Stego message created:")
        print(f"\n{stego}\n")
        print(f"(Length: {len(stego)} characters)")
        print("\n💾 Message saved to stego.txt and copied to clipboard")
    except Exception as e:
        print(f"\n❌ Error creating stego message: {e}")
        return

    # Offer to reveal immediately
    reveal = input("\nWould you like to reveal the message now? (y/n): ").strip().lower()
    if reveal == 'y':
        print_subheader("Step 4: Extracting Hidden Message")

        # Option to use wrong password
        test_wrong = input("Test with wrong password first? (y/n): ").strip().lower()
        if test_wrong == 'y':
            wrong_pass = input("Enter incorrect password: ").strip()
            print(f"\nAttempting to reveal with password '{wrong_pass}'...")
            try:
                wrong_result = revealFunc(stego, wrong_pass)
                print(f"❌ Result: {wrong_result[:100]}...")
                print("(Garbage output - wrong password cannot decrypt!)")
            except Exception as e:
                print(f"❌ Decryption failed: {e}")

        # Reveal with correct password
        print(f"\nRevealing with correct password '{password}'...")
        try:
            revealed = revealFunc(stego, password)
            print(f"\n✅ Revealed secret message: '{revealed}'")

            if revealed == secret:
                print("\n🎉 SUCCESS! Message matches original!")
            else:
                print(f"\n⚠️  Warning: Revealed message differs from original")
        except Exception as e:
            print(f"\n❌ Error revealing message: {e}")


def demo_sanitizer():
    """Interactive sanitizer demonstration"""
    print_header("COVER TEXT SANITIZER")

    print("\nThis demo shows how the sanitizer removes conflicting invisible characters")
    print("from cover text before embedding your secret message.")

    print("\nPre-loaded examples:")
    print("1. Text with zero-width spaces")
    print("2. Text with excessive whitespace")
    print("3. Your own custom text")

    choice = input("\nChoose an option (1-3): ").strip()

    if choice == '1':
        text = "Text\u200bwith\u200bzero\u200bwidth\u200bspaces"
    elif choice == '2':
        text = "Multiple    spaces   and    tabs\there"
    elif choice == '3':
        text = input("Enter your text: ").strip()
    else:
        print("Invalid choice!")
        return

    print(f"\nOriginal text: '{text}'")
    print(f"Original length: {len(text)} characters")

    # Check for invisible characters
    invisible_chars = []
    for char in text:
        if ord(char) in [0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0x202A, 0x202B,
                         0x202C, 0x202D, 0x202E, 0x2060, 0x2061, 0x2062, 0x2063,
                         0x2064, 0xFEFF]:
            invisible_chars.append(f"U+{ord(char):04X}")

    if invisible_chars:
        print(f"Found invisible characters: {', '.join(set(invisible_chars))}")

    # Sanitize
    clean, removed = sanitize_cover_text(text)

    print(f"\nCleaned text: '{clean}'")
    print(f"Cleaned length: {len(clean)} characters")

    if removed:
        print(f"\n✅ Removed: {removed}")
    else:
        print("\n✅ No changes needed - text was already clean!")


def demo_integrity():
    """Interactive integrity verification demonstration"""
    print_header("SHA-256 INTEGRITY VERIFICATION")

    print("\nThis demo shows how tampering with a stego message is detected.")

    secret = input("\nEnter a secret message to protect: ").strip()
    if not secret:
        print("❌ Secret message cannot be empty!")
        return

    password = input("Enter password: ").strip()
    if not password:
        print("❌ Password cannot be empty!")
        return

    cover = input("Enter cover text: ").strip()
    if not cover or len(cover) < 2:
        print("❌ Cover text must be at least 2 characters!")
        return

    # Create stego message
    print("\n📝 Creating stego message with integrity hash...")
    try:
        stego = hideFunc(secret, password, cover)
        print(f"✅ Stego message created (length: {len(stego)})")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test normal retrieval
    print("\n--- Test 1: Normal Retrieval (No Tampering) ---")
    try:
        revealed = revealFunc(stego, password)
        print(f"✅ Successfully revealed: '{revealed}'")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Simulate tampering
    print("\n--- Test 2: Tampered Message Detection ---")
    print("\nChoose tampering method:")
    print("1. Change a character in the middle")
    print("2. Add a character at the end")
    print("3. Remove a character")

    choice = input("\nChoice (1-3): ").strip()

    if choice == '1':
        pos = len(stego) // 2
        tampered = stego[:pos] + "X" + stego[pos+1:]
        print(f"Changed character at position {pos}")
    elif choice == '2':
        tampered = stego + "X"
        print("Added 'X' at the end")
    elif choice == '3':
        tampered = stego[:-1]
        print("Removed last character")
    else:
        print("Invalid choice!")
        return

    print("\n⚠️  Attempting to reveal tampered message...")
    try:
        result = revealFunc(tampered, password)
        if "Integrity" in result or "failed" in result:
            print(f"✅ Tampering detected! Error: {result}")
        else:
            print(f"⚠️  Unexpected result: {result}")
    except Exception as e:
        print(f"✅ Tampering detected! Exception: {type(e).__name__}: {e}")


def demo_randomized_mapping():
    """Interactive randomized mapping demonstration"""
    print_header("RANDOMIZED CHARACTER MAPPING")

    print("\nThis demo shows how different passwords produce different character mappings.")
    print("This makes statistical analysis harder and improves security.")

    print("\nEnter up to 3 passwords to compare their mappings:")

    passwords = []
    for i in range(3):
        pwd = input(f"Password {i+1} (or press Enter to skip): ").strip()
        if pwd:
            passwords.append(pwd)
        else:
            break

    if not passwords:
        print("❌ No passwords entered!")
        return

    print("\n" + "-" * 80)
    print("Mapping Comparison:")
    print("-" * 80)

    for pwd in passwords:
        print(f"\nPassword: '{pwd}'")
        ZWC, _ = generate_mapping(pwd)
        mapping_hash = get_mapping_hash(ZWC)
        print(f"Hash: {mapping_hash}")
        chars_used = [f"U+{ord(ZWC[k]):04X}" for k in sorted(ZWC.keys())]
        print(f"Characters: {', '.join(chars_used)}")

    # Test determinism
    if len(passwords) > 0:
        print("\n" + "-" * 80)
        print(f"Determinism Test: Generating mapping for '{passwords[0]}' three times:")
        print("-" * 80)

        hashes = []
        for i in range(3):
            ZWC, _ = generate_mapping(passwords[0])
            hash_val = get_mapping_hash(ZWC)
            hashes.append(hash_val)
            print(f"  Attempt {i+1}: {hash_val}")

        if len(set(hashes)) == 1:
            print("\n✅ All identical - mapping is deterministic!")
        else:
            print("\n❌ Different hashes - something is wrong!")


def main_menu():
    """Display main menu and handle user choices"""
    while True:
        print_header("INTERACTIVE TEXT STEGANOGRAPHY DEMO")
        print("\nThree Security Features:")
        print("  1. Cover Text Sanitization - Removes conflicting invisible characters")
        print("  2. SHA-256 Integrity Verification - Detects message tampering")
        print("  3. Randomized Character Mapping - Password-derived stealth patterns")

        print("\n\nChoose a demo:")
        print("  1. Hide & Reveal Message (Full Workflow)")
        print("  2. Cover Text Sanitizer")
        print("  3. SHA-256 Integrity Verification")
        print("  4. Randomized Character Mapping")
        print("  5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            demo_hide_reveal()
        elif choice == '2':
            demo_sanitizer()
        elif choice == '3':
            demo_integrity()
        elif choice == '4':
            demo_randomized_mapping()
        elif choice == '5':
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice! Please enter 1-5.")

        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
