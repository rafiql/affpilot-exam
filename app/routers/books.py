from fastapi import FastAPI, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas
from .. database import get_db
from . import logs

import redis
import json
from fastapi.encoders import jsonable_encoder 


router = APIRouter(
    prefix="/books",
    tags=['Books']
)


redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@router.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # Check if the data exists in Redis
    cache_key = f"books:{limit}:{skip}:{search}"
    cached_books = redis_client.get(cache_key)
    if cached_books:
        return json.loads(cached_books)

    books = db.query(models.Book).filter(models.Book.title.contains(search)).limit(limit).offset(skip).all()

    # Convert SQLAlchemy objects to Pydantic models
    books_out = [schemas.BookOut.from_orm(book) for book in books]
    # Cache the data for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(jsonable_encoder(books_out)))

    return books_out


@router.post("/", response_model=schemas.BookOut)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):

    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    # Invalidate cache
    keys = redis_client.keys("books:*")
    for key in keys:
        redis_client.delete(key)

    return new_book

#query parameter as ID
@router.get("/book/{id}", response_model=schemas.BookOut)
def get_book(id: int, db: Session = Depends(get_db)):
    
    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        return f"book with id: {id} was not found"

    return book


@router.get("/book/by/{author_name}", response_model=List[schemas.BookByAuthorOut])
def get_books_by_author(author_name: str, db: Session = Depends(get_db)):
    # Fetch the author by name
    author = db.query(models.Author).filter(models.Author.name == author_name).first()

    if not author:
        return f"author with name: {author_name} was not found"

    # Fetch books written by the author
    books = db.query(models.Book).filter(models.Book.author_id == author.id).all()

    return [{"author_name": author.name, "title": book.title, "author_id": author.id} for book in books]



@router.delete("/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):

    book_to_delete = db.query(models.Book).filter(models.Book.id == id)
    book = book_to_delete.first()

    if book == None:
        return f"book with id: {id} was not found"

    db.delete(book)
    db.commit()

    # Invalidate cache
    keys = redis_client.keys("books:*")
    for key in keys:
        redis_client.delete(key)

    return {"detail": "Book is deleted"}


@router.put("/{id}", response_model=schemas.BookOut)
def update_book(id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db)):

    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()

    if book == None:
        return f"book with id: {id} was not found"

    book_query.update(updated_book.dict(), synchronize_session=False)

    db.commit()

    # Invalidate cache
    keys = redis_client.keys("books:*")
    for key in keys:
        redis_client.delete(key)

    return book_query.first()
