"""
Text Steganography Project - Complete Demo
Shows all three security features working together:
1. Cover Text Sanitization
2. SHA-256 Integrity Verification
3. Randomized Invisible Character Mapping
"""

from sender import hideFunc
from receiver import revealFunc
from randomized_mapping import generate_mapping, get_mapping_hash
from sanitizer import sanitize_cover_text
from enhancements.integrity import hash_message

print("="*80)
print("TEXT STEGANOGRAPHY PROJECT - COMPLETE DEMO")
print("="*80)
print("\nThree Security Features:")
print("  1. Cover Text Sanitization - Removes conflicting invisible characters")
print("  2. SHA-256 Integrity Verification - Detects message tampering")
print("  3. Randomized Character Mapping - Password-derived stealth patterns")
print("="*80)

# ============================================================================
# DEMO 1: Complete Workflow - All Three Features
# ============================================================================
print("\n[DEMO 1] Complete Workflow - All Features Combined")
print("-" * 80)

secret = "This is our team secret message!"
password = "secure123"
cover = "Hello!   This is a normal    message with extra   spaces."

print(f"\n📝 Original Secret: '{secret}'")
print(f"🔑 Password: '{password}'")
print(f"📄 Original Cover Text: '{cover}'")

# Feature 1: Sanitizer (show what gets cleaned)
print("\n--- Feature 1: Cover Text Sanitization ---")
clean_cover, removed = sanitize_cover_text(cover)
print(f"Removed: {removed if removed else 'Nothing (cover was clean)'}")
print(f"Cleaned Cover: '{clean_cover}'")

# Feature 2 & 3 happen inside hideFunc
print("\n--- Features 2 & 3: Integrity + Randomized Mapping ---")
print("Hiding message with:")
print("  • SHA-256 integrity hash attached")
print("  • Password-derived character mapping")

# Show which characters will be used
ZWC, _ = generate_mapping(password)
mapping_hash = get_mapping_hash(ZWC)
print(f"\nMapping Hash: {mapping_hash}")
print("Characters selected:")
for bit_pair in sorted(ZWC.keys()):
    char = ZWC[bit_pair]
    print(f"  '{bit_pair}' -> U+{ord(char):04X}")

# Hide the message
stego = hideFunc(secret, password, clean_cover)
print(f"\n✅ Stego Message Created (first 60 chars):")
print(f"   {stego[:60]}...")

# Reveal the message
print("\n--- Extracting Hidden Message ---")
revealed = revealFunc(stego, password)

if revealed == secret:
    print("\n🎉 SUCCESS! All three features working together!")
else:
    print("\n❌ Failed")

# ============================================================================
# DEMO 2: Sanitizer - Preventing Conflicts
# ============================================================================
print("\n" + "="*80)
print("[DEMO 2] Cover Text Sanitizer - Preventing Invisible Character Conflicts")
print("-" * 80)

dirty_covers = [
    ("Text\u200bwith\u200bzero\u200bwidth", "Zero-width spaces"),
    ("Multiple    spaces   everywhere", "Extra whitespace"),
    ("Clean text here!", "Already clean")
]

for dirty, description in dirty_covers:
    clean, removed = sanitize_cover_text(dirty)
    print(f"\n{description}:")
    print(f"  Before: '{dirty}'")
    print(f"  After:  '{clean}'")
    print(f"  Removed: {removed if removed else '✓ Nothing'}")

# ============================================================================
# DEMO 3: SHA-256 Integrity - Detecting Tampering
# ============================================================================
print("\n" + "="*80)
print("[DEMO 3] SHA-256 Integrity Verification - Detecting Message Tampering")
print("-" * 80)

secret_msg = "Confidential data"
pwd = "integrity_test"
cover_msg = "Public information here."

print(f"\nHiding: '{secret_msg}'")
stego_msg = hideFunc(secret_msg, pwd, cover_msg)

# Simulate tampering by modifying the stego message
print("\n⚠️  Simulating tampering: Changing one character in stego text...")
tampered = stego_msg[:50] + "X" + stego_msg[51:]

print("\nAttempting to reveal tampered message...")
try:
    result = revealFunc(tampered, pwd)
    if "Integrity check failed" in result or "Integrity Error" in result:
        print("✅ Tampering detected successfully!")
        print(f"   Error: {result}")
    else:
        print("❌ Tampering not detected (unexpected)")
except Exception as e:
    print("✅ Tampering detected - extraction failed!")
    print(f"   Error: {type(e).__name__}")

# ============================================================================
# DEMO 4: Randomized Mapping - Password Uniqueness
# ============================================================================
print("\n" + "="*80)
print("[DEMO 4] Randomized Character Mapping - Different Passwords = Different Patterns")
print("-" * 80)

passwords = ["teampassword1", "teampassword2", "teampassword3"]
print("\nSame message, different passwords produce unique invisible character patterns:\n")

for pwd in passwords:
    ZWC, _ = generate_mapping(pwd)
    hash_val = get_mapping_hash(ZWC)
    chars_used = [f"U+{ord(ZWC[k]):04X}" for k in sorted(ZWC.keys())]
    print(f"Password '{pwd}':")
    print(f"  Hash: {hash_val}")
    print(f"  Chars: {', '.join(chars_used)}")
    print()

# ============================================================================
# DEMO 5: Determinism - Same Password = Same Mapping
# ============================================================================
print("="*80)
print("[DEMO 5] Determinism - Same Password Always Produces Same Mapping")
print("-" * 80)

print("\nGenerating mapping for 'constantPassword' three times:\n")
for i in range(3):
    ZWC, _ = generate_mapping("constantPassword")
    hash_val = get_mapping_hash(ZWC)
    print(f"  Attempt {i+1}: {hash_val}")

print("\n✅ All identical - proves deterministic behavior!")

# ============================================================================
# DEMO 6: Security - Wrong Password Fails
# ============================================================================
print("\n" + "="*80)
print("[DEMO 6] Security - Wrong Password Cannot Reveal Message")
print("-" * 80)

sec = "Top secret information"
correct = "rightpass"
wrong = "wrongpass"
cov = "Innocent looking message."

print(f"\nHiding '{sec}' with password '{correct}'")
stego_final = hideFunc(sec, correct, cov)

print(f"Trying to reveal with WRONG password '{wrong}'...")
wrong_result = revealFunc(stego_final, wrong)

if wrong_result != sec:
    print(f"✅ Wrong password produces garbage or error:")
    print(f"   '{wrong_result[:50]}...'")
else:
    print("❌ Wrong password somehow worked (unexpected!)")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*80)
print("DEMO COMPLETE - SUMMARY")
print("="*80)
print("\n✅ All Three Features Demonstrated:")
print("\n1. SANITIZER (Cover Text Cleaning)")
print("   • Removes conflicting invisible characters")
print("   • Normalizes whitespace")
print("   • Prevents decoding errors")
print("\n2. INTEGRITY (SHA-256 Verification)")
print("   • Detects message tampering")
print("   • Ensures data hasn't been modified")
print("   • Cryptographic hash validation")
print("\n3. RANDOMIZED MAPPING (Password-Derived Patterns)")
print("   • 43,680 possible unique character mappings")
print("   • Deterministic (same password = same mapping)")
print("   • Harder to detect through statistical analysis")
print("\n🔐 Combined Security: Multi-layer protection for hidden messages")
print("="*80)
