from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str

class UserRead(UserBase):
    id: int