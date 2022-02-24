from cryptography.fernet import Fernet


class AccessEncrypted():

    def __init__(self, filename, key):
        self.filename = filename
        self.key = key
        self.fernet = Fernet(key)

    def __enter__(self):
        self.file = open(self.filename, "r+b")
        encrypted = self.file.read()
        original = self.fernet.decrypt(encrypted)
        self.file.truncate(0)
        self.file.seek(0)
        self.file.write(original)
        self.file.seek(0)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.seek(0)
        original = self.file.read()
        encrypted = self.fernet.encrypt(original)
        self.file.truncate(0)
        self.file.seek(0)
        self.file.write(encrypted)
        self.file.close()
