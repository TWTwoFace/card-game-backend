from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> bytes:
    salt = gensalt()
    hashed_password = hashpw(bytes(password), salt)
    return hashed_password


def check_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(bytes(password), hashed_password)
