from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> str:
    salt = gensalt()
    hashed_password = hashpw(bytes(password, 'utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(bytes(password, 'utf-8'), hashed_password.encode('utf-8'))
