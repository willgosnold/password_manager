import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from getpass import getpass
from context import AccessEncrypted

import pandas as pd

salt = b"qwerty"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(getpass().encode('utf-8')))
fernet = Fernet(key)

with AccessEncrypted("vault.csv", key) as file:
    df = pd.read_csv(file)

print(df)


def encrypt_file(file):
    with open(file, 'rb') as f:
        original = f.read()
    encrypted = fernet.encrypt(original)
    with open(file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file(file):
    with open(file, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    original = fernet.decrypt(encrypted)
    with open(file, 'wb') as file:
        file.write(original)


# encrypt_file("vault.csv")
