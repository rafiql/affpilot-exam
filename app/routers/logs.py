import logging
from sqlalchemy import event
from app.models import Book

# Configure logging to output to a file
logging.basicConfig(
    filename="book_creation.log",
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

@event.listens_for(Book, "after_insert")
def log_new_book(mapper, connection, target):
    # Create a log entry whenever a book is created
    log_message = f"Action: CREATE - Title: {target.title}, Author ID: {target.author_id}"
    logging.info(log_message)


# Log deletion event
@event.listens_for(Book, "after_delete")
def log_delete_book(mapper, connection, target):
    log_message = f"Action: DELETE - Title: {target.title}, Author ID: {target.author_id}"
    logging.info(log_message)