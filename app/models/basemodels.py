from enum import Enum
from dataclasses import dataclass
from datetime import datetime, date
from abc import ABC


class BaseModel(ABC):
    pass


class UserRole(Enum):
    ADMIN = "admin"
    OWNER = "owner"
    USER = "user"

@dataclass
class EventModel(BaseModel):
    created: datetime
    user_id: int
    start_dt: date
    end_dt: date
    name: str
    mode: str
    place: str
    description: str
    duration: int

    def dict(self):
        return {
            "created": self.created,
            "user_id": self.user_id,
            "start_dt": self.start_dt,
            "end_dt": self.end_dt,
            "name": self.name,
            "mode": self.mode,
            "place": self.place,
            "description": self.description,
            "duration": self.duration,
        }

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"User ID: {self.user_id}\n"
            f"Created: {self.created}\n"
            f"Start Date: {self.start_dt}\n"
            f"End Date: {self.end_dt}\n"
            f"Name: {self.name}\n"
            f"Mode: {self.mode}\n"
            f"Place: {self.place}\n"
            f"Description: {self.description}\n"
            f"Duration: {self.duration} days"
        )

@dataclass
class UsersModel(BaseModel):
    id: int
    user_id: int
    created: datetime
    role: UserRole
    first_name: str
    last_name: str
    username: str

    def __post_init__(self):
        self.role = UserRole(self.role)


class Action(str, Enum):
    DELETE = "delete"
    POST = "post"