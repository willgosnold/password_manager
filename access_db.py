import sqlite3


class AccessDB():

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()
        if exc_type is sqlite3.IntegrityError:
            print("You already have a password for this site.")
            return True
