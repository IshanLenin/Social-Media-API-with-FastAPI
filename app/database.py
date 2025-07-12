from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

def get_db(): # Dependency to get a database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


''' 
# This code attempts to connect to a PostgreSQL database using psycopg2.
# It will keep retrying every 2 seconds until a successful connection is established.

while True: 
    try: # Establishing a connection to the PostgreSQL database
        #conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                           password='CHACHU2206',cursor_factory=RealDictCursor)
    # Creating a cursor object to execute SQL queries
        cursor = conn.cursor()
        print("Database connection successful")
        break  # Exit the loop if connection is successful
    #except Exception as error:
        print("Database connection failed")
        print(f"Error: {error}")
        time.sleep(2)  # Wait for 2 seconds before retrying
'''