from pydantic import BaseModel
from typing import Optional

# Author schemas
class AuthorOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    name: str

# Book schemas
class BookBase(BaseModel):
    title: str
    author_id: int


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    author: AuthorOut  # Display author details in response

    class Config:
        orm_mode = True


class BookByAuthorOut(BookBase):
    author_name: str
    title: str

    class Config:
        orm_mode = True
