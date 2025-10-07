from pydantic import BaseModel, ValidationError, Field, field_validator, model_validator
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

# Creating model variations with class inheritance
class PostBase(BaseModel):
    title: str
    content: str
    # we can also define functions in pydantic models
    def excerpt(self):
        return f"{self.content[:140]}..."

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id : int

class Post(PostBase):
    id : int
    nb_views: int = 0

# Custom validation 
## Field level validation
# Import field_validator from pydantic 
from datetime import date
class Customer(BaseModel):
    firstname: str
    lastname: str
    birthdate: date

    @field_validator("birthdate")
    def valid_birthdate(cls, v:date):
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You're too old")
        else:
            print("You are eligible to have account")
        return v

c1 = Customer(firstname="jim", lastname="kim", birthdate= "1999-11-01" )

## Object level validation
# Import root_validator decorator from pydantic
class UserRegistration(BaseModel):
    username: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def password_match(cls, values):
        password = values.password
        confirm_password = values.confirm_password
        if password != confirm_password:
            raise ValueError("passwords doesn't match")
        else:
            print("Account successfully created")
        return values
    
user1 = UserRegistration(username="jhn@mailinator.com", password= "bill", confirm_password="bill" )


# Validating before parsing
class Model(BaseModel):
    values: list[int]

    @field_validator("values", mode="before")
    def splitter(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v
    
m = Model(values="1,2,3")
print(m.values)

# Working with Pydantic objects
# Converting an object into dictionary
person1 = Person(first_name="Khan", last_name="Khan", gender="male", birthdate="2003-03-03", age = 21, interests=["Music"],
                 address={"street": "Lord",
                          "postal_code": "2342423",
                          "city": "New York",
                          "country": "USA"})
person_dict = person1.model_dump() # p1 is created at start
print(person_dict["address"]["street"])

## Including and Excluding 
person_include = person1.model_dump(include={"first_name", "last_name"})
print(person_include)

person_exclude = person1.model_dump(exclude={'age', "address"})
print(person_exclude)

### sub-dictionary level including and excluding
person_subdict = person1.model_dump(include={"first_name": ...,
                                             "last_name": ...,
                                             "address": {'city', "country"}})
print(person_subdict)
