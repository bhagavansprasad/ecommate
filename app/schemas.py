from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    role: str
    client: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class MovieSchema(BaseModel):
    id: int
    title: str
    director: str
    genre: str
    year: int

    class Config:
        orm_mode = True

# Shared properties for Movie
class MovieBase(BaseModel):
    title: str
    director: str
    genre: str
    year: int

# Properties to receive on Movie creation
class MovieCreate(MovieBase):
    pass

# Properties to return via API
class MovieResponse(MovieBase):
    id: int

    class Config:
        orm_mode = True
