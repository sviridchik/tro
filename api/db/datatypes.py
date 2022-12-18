from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseDataclass:
    id: int = None

    @property
    def pk(self):
        return self.id


@dataclass
class User(BaseDataclass):
    username: str = None
    email: str = None
    password: str = None
    is_active: bool = None

    is_authenticated = True


@dataclass
class Token(BaseDataclass):
    key: str = None
    user: User = None
    created: datetime = None


@dataclass
class Patient(BaseDataclass):
    user: User = None
    first_name: str = None
    last_name: str = None
    age: int = None
    phone: int = None

    def __str__(self):
        return self.first_name + " " + self.last_name


@dataclass
class Guardian(BaseDataclass):
    banned: bool = None
    is_send: bool = None
    relationship: bool = None
    user: User = None
    first_name: str = None
    last_name: str = None
    phone: int = None
    care_about: Patient = None

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)
