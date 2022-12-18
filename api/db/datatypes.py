from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    username: str
    email: str
    password: str
    is_active: bool
    id: int = None


@dataclass
class Token:
    key: str
    user: User
    created: datetime
    id: int = None
