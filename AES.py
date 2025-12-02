import binascii
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

def get_private_key(password):
    salt = b"this is a salt"
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key

def encrypt(passwrd, message):
    key = get_private_key(passwrd)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(bytes(message, "utf-8"))
    msg = binascii.hexlify(msg)
    encryptedMsg = msg.decode("ascii")
    return encryptedMsg

def decrypt(passwrd, message):
    key = get_private_key(passwrd)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = cipher.decrypt(binascii.unhexlify(bytes(message, "utf-8")))[len(iv):]
    decMsg = msg.decode("utf-8")
    return decMsg