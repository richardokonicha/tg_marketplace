from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    "User Class Repr"
    user_id: int = 0
    role: str = ""  # vendor, buyer


@dataclass
class Product:
    "Product Repr"
    name: str = ""
    owner: int = ""  # User.user_id
    # more fields need


@dataclass
class Order:
    "Order repr for a transaction"
    created: str = ""  # tiome string on if creation
