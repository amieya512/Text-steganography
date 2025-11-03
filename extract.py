## EXTRACTING ALGORITHM
import math
from enhancements.randomized_mapping import generate_random_mapping

# --- Use the same character set and generate a random mapping ---
ZWC, ZWC_reverse = generate_random_mapping()

def xor(a, b, n):
    ans = ""
    for i in range(n):
        ans += "0" if a[i] == b[i] else "1"
    return ans

def binaryToDecimal(n):
    return int(n, 2)

SM_extract = ""
MR_SK = "121"
hashed_SM_binary_extract = ""

def extractFunc(CM_HM):
    """
    Extracts the hidden secret message from the cover message (CM_HM)
    using the current randomized mapping of zero-width Unicode characters.
    """
    global SM_extract, MR_SK, hashed_SM_binary_extract, ZWC_reverse
    SM_extract = ""
    hashed_SM_binary_extract = ""

    for letter in CM_HM:
        if letter in ZWC_reverse:
            hashed_SM_binary_extract += ZWC_reverse[letter]

    MS_SK_extract = hashed_SM_binary_extract[0:8]
    MR_SK_binary = '{0:08b}'.format(int(MR_SK))

    if MS_SK_extract == MR_SK_binary:
        hashed_SM_binary_extract = hashed_SM_binary_extract[8:]
        LSK_extract = len(MR_SK_binary)
        P = 0 if (len(hashed_SM_binary_extract) % LSK_extract) == 0 else 1
        NC_extract = int((len(hashed_SM_binary_extract) / LSK_extract) + P)
        hash_position_bits_extract = NC_extract * MR_SK_binary
        SM_binary_extract = xor(
            hashed_SM_binary_extract, hash_position_bits_extract, len(hashed_SM_binary_extract)
        )

        while len(SM_binary_extract) >= 12:
            alpha_beta = SM_binary_extract[0:12]
            SM_binary_extract = SM_binary_extract[12:]
            alpha_extract = alpha_beta[0:6]
            beta_extract = alpha_beta[6:12]
            alpha_final = binaryToDecimal(alpha_extract)
            beta_final = binaryToDecimal(beta_extract)
            n_final = ((pow(2, alpha_final) * (2 * beta_final + 1)) - 1)
            SM_extract += chr(n_final)

    print("Encrypted secret message received:", SM_extract)
    return SM_extract


 
