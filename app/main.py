from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import books, authors
from .config import settings

#for migratiion into db table
from app.database import Base, engine  
from app.models import Author, Book


app = FastAPI()

#for migratiion into db table
Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(authors.router)



@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
