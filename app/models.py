from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    published_date = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey(
        "authors.id", ondelete="CASCADE"), nullable=False)

    author = relationship("Author")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    dob = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

