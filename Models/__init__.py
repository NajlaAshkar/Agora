from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from .DB_metadata import pengine

def validate_database():
     if not database_exists(pengine.url): # Checks for the first time
            create_database(pengine.url)     # Create new DB
            print("New Database Created"+database_exists(pengine.url))  # Verifies if database is there or not.
     else:
            print("Database Already Exists")


# if __name__ == '__main__':
#    validate_database()
