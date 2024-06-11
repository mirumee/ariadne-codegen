from enum import Enum


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    GUEST = "GUEST"
