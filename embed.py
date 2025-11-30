## EMBEDDING ALGORITHM

import math

# Function to check Log base 2
def Log2(x):
    if x == 0:
        return False
    return (math.log10(x) / math.log10(2))

# Function to check if x is power of 2
def isPowerOfTwo(n):
    return (math.ceil(Log2(n)) == math.floor(Log2(n)))

# XOR of the two Binary Strings
def xor(a, b, n):
    ans = ""
    for i in range(n):
        if a[i] == b[i]:
            ans += "0"
        else:
            ans += "1"
    return ans

def binaryToDecimal(n):
    return int(n, 2)

MS_SK = "121"  # extracted from 12.15
SM_binary = ""


def embedFunc(SM, CM, ZWC, ZWC_reverse):
    """
    Embeds a secret message into cover text using randomized character mapping.

    Args:
        SM: Secret message (encrypted)
        CM: Cover message
        ZWC: Character mapping dictionary (binary pairs -> invisible chars)
        ZWC_reverse: Reverse mapping dictionary

    Returns:
        Stego message with embedded secret
    """
    global MS_SK, SM_binary
    # Reset global variable for each embedding
    SM_binary = ""

    for letter in SM:
        n = ord(letter)
        factors = []
        for i in range(1, n + 1):
            if (n + 1) % i == 0:
                factors.append(i)

        odd_factors_list = []
        for f in factors:
            if f % 2 != 0:
                odd_factors_list.append(f)

        alpha = -99999
        for odd_factor in odd_factors_list:
            power_exists = isPowerOfTwo(int((n + 1) / odd_factor))
            if power_exists:
                power = math.log10(int((n + 1) / odd_factor)) / math.log10(2)
                if power > alpha:
                    alpha = int(power)

        if alpha == -99999 and n % 2 == 0:
            alpha = 0

        alpha_binary = "{0:06b}".format(alpha)
        beta = int((((n + 1) / pow(2, alpha)) - 1) / 2)
        beta_binary = "{0:06b}".format(beta)
        SM_binary = SM_binary + alpha_binary + beta_binary

    MS_SK_binary = "{0:08b}".format(int(MS_SK))
    LSK = len(MS_SK_binary)

    if len(SM_binary) % LSK == 0:
        P = 0
    else:
        P = 1

    NC = int((len(SM_binary) / LSK) + P)
    hash_position_bits = NC * MS_SK_binary
    hashed_SM_binary = xor(SM_binary, hash_position_bits, len(SM_binary))

    HM_SK = ""
    i = 0
    while i < len(MS_SK_binary) - 1:
        x = MS_SK_binary[i] + MS_SK_binary[i + 1]
        HM_SK += ZWC[x]
        i += 2

    HM_ZWC = ""
    i = 0
    while i < len(hashed_SM_binary) - 1:
        x = hashed_SM_binary[i] + hashed_SM_binary[i + 1]
        HM_ZWC += ZWC[x]
        i += 2

    HM = HM_SK + HM_ZWC
    CM_HM = CM[:-1] + HM + CM[-1]
    return CM_HM
