import string
from enum import Enum
from random import shuffle
from itertools import chain
from secrets import choice, randbelow
import sqlite3


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
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE passwords(site UNIQUE, password)")
    con.close()


def add_to_vault(site, password):
    try:
        con = sqlite3.connect("vault.db")
        cur = con.cursor()
        cur.execute("INSERT INTO passwords VALUES(?, ?)", (site, password))
        con.commit()
        con.close()
    except sqlite3.IntegrityError:
        print(f"You already have a password for {site}.")
        if con:
            con.close()


def show_all():
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    for i, row in enumerate(cur.execute("SELECT * FROM passwords")):
        print(f"{i+1}) {row[0]}: {row[1]}")
    con.close()


def retrieve(site):
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    for row in cur.execute("SELECT password FROM passwords where site=?", (site,)):
        password = row
    con.close()
    return password[0]


def delete(site):
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    cur.execute("DELETE from passwords where site=?", (site,))
    con.commit()
    con.close()


def purge_table():
    con = sqlite3.connect("vault.db")
    cur = con.cursor()
    cur.execute("DELETE from passwords")
    con.commit()
    con.close()


if __name__ == '__main__':
    sites = ["amazon", "facebook", "google", "twitter", "instagram"]
    for site in sites:
        add_to_vault(site, generate())
    # print(retrieve('amazon'))
    # delete('facebook')
    # purge_table()
    show_all()
