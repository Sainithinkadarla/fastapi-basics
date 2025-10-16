from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

    class Config():
        from_attributes = True

class UserRead(UserBase):
    id: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_passwd: str

class UserUpdate(UserBase):
    pass