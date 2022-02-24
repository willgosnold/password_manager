import base64
from getpass import getpass
import pandas as pd

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from context import AccessEncrypted


salt = b"qwerty"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(getpass().encode('utf-8')))
fernet = Fernet(key)


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
# decrypt_file("vault.csv")


def add_password(site, password):
    with AccessEncrypted("vault.csv", key) as file:
        df = pd.read_csv(file, index_col=0)
        df.loc[site] = password
        df.to_csv("vault.csv")
    return password


# print(add_password("google", "emmzybabez<3"))


def retrieve_password(site):
    with AccessEncrypted("vault.csv", key) as file:
        df = pd.read_csv(file, index_col=0)
        password = df.loc[site].password
    return password


# print(retrieve_password("google"))


def delete_password(site):
    with AccessEncrypted("vault.csv", key) as file:
        df = pd.read_csv(file, index_col=0)
        df = df.drop(site)
        df.to_csv("vault.csv")
    print(f"Password for {site} deleted.")


# delete_password("twitter")


def show_all():
    with AccessEncrypted("vault.csv", key) as file:
        df = pd.read_csv(file, index_col=0)
        for index, row in df.iterrows():
            print(index, row['password'])


show_all()


def purge_vault():
    with AccessEncrypted("vault.csv", key) as file:
        df = pd.read_csv(file, index_col=0)
        df = df[0:0]
        df.to_csv("vault.csv")
    print("Vault deleted.")


# purge_vault()
