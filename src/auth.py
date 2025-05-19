from datetime import datetime, timezone
from typing import Optional

from fastapi import Header, Depends
from jwt import encode, decode, InvalidTokenError

from src.config.env import JWT_ACCESS_KEY, JWT_ALGORITHM


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc).second
    to_encode.update({"expire_at": expire})
    token = encode(payload=to_encode, key=JWT_ACCESS_KEY, algorithm=JWT_ALGORITHM)
    return token


def validate_user(uid: int, token: Optional[str]):
    if token is None:
        return False
    try:
        payload = decode(jwt=token, key=JWT_ACCESS_KEY, algorithms=JWT_ALGORITHM)
        return str(uid) == str(payload['id'])
    except InvalidTokenError as e:
        return False


def get_current_token(token: str = Header(alias='x-auth-static-token')):
    return token


def get_current_user_id(token: Optional[str] = Depends(get_current_token)) -> Optional[int]:
    if token is None:
        return None
    try:
        payload = decode(jwt=token, key=JWT_ACCESS_KEY, algorithms=JWT_ALGORITHM)
        return payload['id']
    except InvalidTokenError as e:
        return None
