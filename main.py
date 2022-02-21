import string
import secrets


def generate(length=16, letters=True, mix_case=True, digits=True, special=True):
    chars = ""
    if letters:
        if mix_case:
            chars += string.ascii_letters
        else:
            chars += string.ascii_lowercase
    if digits:
        chars += string.digits
    if special:
        chars += string.punctuation
    while True:
        password = "".join(secrets.choice(chars) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in password for c in string.punctuation)):
            break
    return password


database = {}


print(database)

database.setdefault("facebook", generate())
database.setdefault("instagram", generate())

print(database)
