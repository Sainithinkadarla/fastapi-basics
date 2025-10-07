from pydantic import BaseModel, ValidationError, Field
from enum import Enum
from datetime import date

# defining field and their types
class Gender(str, Enum):
    male = "male"
    ffemale = "female"
    non_binary = "non_binary"


class Address(BaseModel):
    street: str
    postal_code: str
    city: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    age: int
    interests: list[str]
    address: Address

print("p1 innitiating....")
try: 
    p1 = Person(
        first_name= "john",
        last_name = "doe",
        age = 43,
        gender="female",
        birthdate = '2004-02-14',
        interests= ["Music", "Games"],
        address= {
            "street": "efdfdafsd",
            "postal_code": "500033",
            "city": "hyderabad",
            "country": "India"
        }
    )
    print(p1)
except ValidationError as e:
    print(e)

print("p2 innitiating....")
try: 
    p2 = Person(
        first_name= "john",
        last_name = "doe",
        age = 43,
        gender="ffemale",
        birthdate = '14-02-2004',
        interests= ["Music", "Games"]
    )
    print(p2)
except ValidationError as e:
    print(e)

# Optional values and default values
class UserProfile(BaseModel):
    nickname: str
    location: str | None = None
    newsletter: bool = True

user1 = UserProfile(nickname="sam")
print(user1)
user2 = UserProfile(nickname="kim", location= "LA", newsletter=False)
print(user2)


## What happens if dynamic values are used as default values
import datetime, time
class Model(BaseModel):
    date: datetime.datetime = datetime.datetime.now()
o1 = Model()
print(o1)

time.sleep(1)

o2 = Model()
print(o2)

print(o1.date < o2.date)


## Field function
# import Field  function from pydantic package
class Officer(BaseModel):
    firstname: str = Field(..., min_length=3) 
    lastname: str = Field(..., min_length=3)
    age: int | None = Field(None, ge=0, le=120)

of1 = Officer(firstname="jim", lastname="Khan")
print(of1)

## Dynamic default values
def genre_factory():
    return ["Music", "Tech", "Art"]

class Post(BaseModel):
    title: str = Field(..., min_length=3)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    genre: list[str] = Field(default_factory=genre_factory)
    category: list[str] = Field(default_factory=list)

p1 = Post(title="An article")
print(p1)

p2 = Post(title="An article of second")
print(p2)

print(p1.timestamp < p2.timestamp)

# Validating Email addresses and URLs with Pydantic types
# install email-validator package
# import HTTPUrl and EmailStr from pydantic
from pydantic import EmailStr, HttpUrl

class User(BaseModel):
    email: EmailStr
    website: HttpUrl

try:
    u1 = User(email= "john@gss.com", website="https://google.com")
    print(u1)
except ValidationError as e:
    print(e)