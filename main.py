import string
from enum import Enum
from random import shuffle
from itertools import chain
from secrets import choice, randbelow
import sqlite3
from access_db import AccessDB


class CharTypes(Enum):
    UPPER = string.ascii_uppercase     # Capital
    LOWER = string.ascii_lowercase     # Small
    DIGITS = string.digits             # Digits
    SPECIAL = string.punctuation       # Special


def generate(min_length=14, max_length=20, upper=1, lower=1, digits=1, special=1):
    char_counts = (upper, lower, digits, special)
    num_chars = sum(char_counts)
    target_length = min_length + randbelow(max_length - min_length + 1)

    # Get list of enums to pass `secrets.choice` call excluding
    # those where arg=0.
    char_type_enums = [
        char_type for i, char_type in enumerate(CharTypes) if char_counts[i]]

    # List of password elements comprised of: mandatory chars + filler
    elements = list(
        chain(*([c_type] * num for c_type, num in zip(CharTypes, char_counts)),
              (choice(char_type_enums) for _ in range(target_length - num_chars))))

    shuffle(elements)
    password = "".join(choice(element.value) for element in elements)
    return password


def create_db():
    with AccessDB("vault.db") as db:
        db.execute(
            ("CREATE TABLE if not exists passwords(site UNIQUE, password)"))


def add_password(site, password):
    with AccessDB("vault.db") as db:
        db.execute("INSERT INTO passwords VALUES(?, ?)", (site, password))
        return password


def show_all():
    with AccessDB("vault.db") as db:
        for i, row in enumerate(db.execute("SELECT * FROM passwords")):
            print(f"{i+1}) {row[0]}: {row[1]}")


def retrieve_password(site):
    with AccessDB("vault.db") as db:
        for row in db.execute("SELECT password FROM passwords where site=?", (site,)):
            password = row
            return password[0]


def delete_password(site):
    with AccessDB("vault.db") as db:
        db.execute("DELETE from passwords where site=?", (site,))


def purge_table():
    with AccessDB("vault.db") as db:
        db.execute("DELETE from passwords")


if __name__ == '__main__':
    create_db()
    while True:
        func = input(
            '''What would you like to do? \n
            (add_password | retrieve_password | delete_password | close) ''')
        print(func)
        site = input("Which site? ")
        if func == "add_password":
            print(add_password(site, generate()))
        elif func == "retrieve_password":
            print(retrieve_password(site))
        elif func == "delete_password":
            delete_password(site)
            print(f"Password for {site} deleted.")
        elif func == "close":
            break
        else:
            print("Please enter a valid command.")

    # sites = ["amazon", "facebook", "google", "twitter", "instagram"]
    # for site in sites:
    #     add_password(site, generate())

    # print(retrieve_password('amazon'))
    # delete_password('facebook')
    # purge_table()
    # add_password("amazon", generate())
    # show_all()
