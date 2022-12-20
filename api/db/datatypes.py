from dataclasses import dataclass
import datetime
from typing import List


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

    patient: 'Patient' = None

    is_authenticated = True


@dataclass
class Token(BaseDataclass):
    key: str = None
    user: User = None
    created: datetime.datetime = None


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


@dataclass
class Doctor(BaseDataclass):
    first_name: str = None
    last_name: str = None
    specialty: str = None
    patient: Patient = None


@dataclass
class DoctorVisit(BaseDataclass):
    date: datetime.datetime = None
    doctor: Doctor = None
    patient: Patient = None


@dataclass
class TimeTable(BaseDataclass):
    time: datetime.time = None
    schedule_id: int = None


@dataclass
class Schedule(BaseDataclass):
    cycle_start: datetime.date = None
    cycle_end: datetime.date = None
    frequency: int = None
    timesheet: List[TimeTable] = None


@dataclass
class Cure(BaseDataclass):
    patient: Patient = None
    title: str = None
    dose: float = None
    dose_type: str = None
    schedule: Schedule = None
    type: str = None
    strict_status: bool = None

    food: str = None

    def __str__(self):
        return self.title
