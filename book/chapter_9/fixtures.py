from pydantic import BaseModel
from datetime import date
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "Female"

class Address(BaseModel):
    street_no: str
    postal_code: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    age: int
    address: Address
    gender: Gender