from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AuthorOut(BaseModel):
    id: int
    name: Str
    
    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    name: Str


class BookBase(BaseModel):
    title: str
    

class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int
    author: AuthorOut

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    Book: Book

    class Config:
        orm_mode = True



