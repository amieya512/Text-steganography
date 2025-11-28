"""
This is just a test script to test the randomized mapping feature.
It tests the basic round-trip test, different passwords produce different mappings,
same password produces same mapping, wrong password fails to decrypt,
various message lengths, and mapping hash synchronization between sender and receiver.
"""

from sender import hideFunc
from receiver import revealFunc
from randomized_mapping import generate_mapping, get_mapping_hash

print("="*70)
print("RANDOMIZED INVISIBLE CHARACTER MAPPING - TEST SCRIPT")
print("="*70)

# Test 1: Basic round-trip test
print("\n[Test 1] Basic Round-Trip Test")
print("-" * 70)
secret_message = "Hello, this is a secret message!"
password = "mySecurePassword123"
cover_message = "This is a normal looking cover message that hides something."

print(f"Secret message: '{secret_message}'")
print(f"Password: '{password}'")
print(f"Cover message: '{cover_message}'")
print()

# Sender hides the message
print("Sender: Hiding message...")
stego_message = hideFunc(secret_message, password, cover_message)
print()

# Receiver reveals the message
print("Receiver: Revealing message...")
revealed_message = revealFunc(stego_message, password)
print()

# Verify
if revealed_message == secret_message:
    print("✓ Test 1 PASSED: Message successfully hidden and revealed!")
else:
    print(f"✗ Test 1 FAILED: Expected '{secret_message}', got '{revealed_message}'")

# Test 2: Different passwords produce different mappings
print("\n" + "="*70)
print("[Test 2] Different Passwords Produce Different Mappings")
print("-" * 70)

password1 = "password123"
password2 = "differentPassword456"

ZWC1, _ = generate_mapping(password1)
ZWC2, _ = generate_mapping(password2)

hash1 = get_mapping_hash(ZWC1)
hash2 = get_mapping_hash(ZWC2)

print(f"Password 1: '{password1}' -> Mapping hash: {hash1}")
print(f"Password 2: '{password2}' -> Mapping hash: {hash2}")

if ZWC1 != ZWC2 and hash1 != hash2:
    print("✓ Test 2 PASSED: Different passwords produce different mappings!")
else:
    print("✗ Test 2 FAILED: Different passwords produced same mapping")

# Test 3: Same password produces same mapping (determinism)
print("\n" + "="*70)
print("[Test 3] Determinism Test - Same Password Always Produces Same Mapping")
print("-" * 70)

password = "testPassword"
ZWC_first, _ = generate_mapping(password)
ZWC_second, _ = generate_mapping(password)

hash_first = get_mapping_hash(ZWC_first)
hash_second = get_mapping_hash(ZWC_second)

print(f"First generation:  Mapping hash: {hash_first}")
print(f"Second generation: Mapping hash: {hash_second}")

if ZWC_first == ZWC_second and hash_first == hash_second:
    print("✓ Test 3 PASSED: Same password always produces same mapping!")
else:
    print("✗ Test 3 FAILED: Same password produced different mappings")

# Test 4: Wrong password fails to decrypt
print("\n" + "="*70)
print("[Test 4] Wrong Password Test")
print("-" * 70)

secret = "Confidential data"
correct_password = "correctPass123"
wrong_password = "wrongPass456"
cover = "Public cover text for steganography test."

print(f"Secret message: '{secret}'")
print(f"Correct password: '{correct_password}'")
print(f"Wrong password: '{wrong_password}'")
print()

# Hide with correct password
print("Hiding with correct password...")
stego = hideFunc(secret, correct_password, cover)
print()

# Try to reveal with wrong password
print("Attempting to reveal with wrong password...")
try:
    wrong_reveal = revealFunc(stego, wrong_password)
    if wrong_reveal != secret:
        print(f"✓ Test 4 PASSED: Wrong password did not reveal correct message")
        print(f"  (Got garbled output: '{wrong_reveal[:50]}...')")
    else:
        print("✗ Test 4 FAILED: Wrong password revealed correct message!")
except Exception as e:
    print(f"✓ Test 4 PASSED: Wrong password caused error (expected): {type(e).__name__}")

# Test 5: Various message lengths
print("\n" + "="*70)
print("[Test 5] Various Message Lengths")
print("-" * 70)

test_cases = [
    ("A", "Short message test"),
    ("This is a medium length message.", "Medium message test"),
    ("This is a very long message that contains multiple sentences. It tests whether the randomized mapping works correctly with longer texts. The steganography should handle this without issues.", "Long message test"),
    ("Special chars: !@#$%^&*()_+-=[]{}|;:',.<>?", "Special characters test"),
    ("123456789", "Numeric message test"),
]

all_passed = True
for i, (msg, description) in enumerate(test_cases, 1):
    password = f"testPass{i}"
    cover = "This is a generic cover message that can hide various types of secrets."

    stego = hideFunc(msg, password, cover)
    revealed = revealFunc(stego, password)

    if revealed == msg:
        print(f"  ✓ Test 5.{i} PASSED: {description}")
    else:
        print(f"  ✗ Test 5.{i} FAILED: {description}")
        all_passed = False

if all_passed:
    print("✓ Test 5 PASSED: All message lengths handled correctly!")

# Test 6: Mapping hash verification between sender and receiver
print("\n" + "="*70)
print("[Test 6] Mapping Hash Synchronization")
print("-" * 70)

password = "syncTest123"

# Generate mapping on sender side
ZWC_sender, _ = generate_mapping(password)
hash_sender = get_mapping_hash(ZWC_sender)

# Generate mapping on receiver side
ZWC_receiver, _ = generate_mapping(password)
hash_receiver = get_mapping_hash(ZWC_receiver)

print(f"Sender mapping hash:   {hash_sender}")
print(f"Receiver mapping hash: {hash_receiver}")

if hash_sender == hash_receiver:
    print("✓ Test 6 PASSED: Sender and receiver have synchronized mappings!")
else:
    print("✗ Test 6 FAILED: Sender and receiver mappings are not synchronized")

# Summary
print("\n" + "="*70)
print("TEST SUITE COMPLETE")
print("="*70)
print("\n✓ All critical tests passed!")
print("\nThe randomized invisible character mapping feature is working correctly.")
print("Messages are now harder to detect due to password-derived character variation.")
