# enhancements/randomized_mapping.py
import random

# Candidate invisible Unicode characters (Zero-Width characters)
INVISIBLE_CHARS = ['\u200B', '\u200C', '\u200D', '\u2060']  # ZWSP, ZWNJ, ZWJ, WJ

def generate_random_mapping(seed=None):
    """
    Randomize mapping of 2-bit binary values ('00','01','10','11')
    to invisible Unicode characters each session.
    Returns both mapping and reverse mapping dicts.
    """
    if seed:
        random.seed(seed)
    shuffled = random.sample(INVISIBLE_CHARS, len(INVISIBLE_CHARS))
    ZWC = {"00": shuffled[0], "01": shuffled[1], "10": shuffled[2], "11": shuffled[3]}
    ZWC_reverse = {v: k for k, v in ZWC.items()}
    return ZWC, ZWC_reverse

if __name__ == "__main__":
    ZWC, ZWC_reverse = generate_random_mapping()
    print("Session mapping:")
    for k, v in ZWC.items():
        print(k, "→", hex(ord(v)))
