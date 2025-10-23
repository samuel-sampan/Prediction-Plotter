from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

Base = declarative_base()

class UserEntry(Base):
    __tablename__ = 'user_entries'
    
    id = Column(Integer, primary_key=True)
    entry_number = Column(Integer)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///user_data.db')

# Fix for Render PostgreSQL URLs
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_entry(entry_number, value):
    """Save a user entry to the database"""
    session = Session()
    try:
        new_entry = UserEntry(entry_number=entry_number, value=value)
        session.add(new_entry)
        session.commit()
        print(f"Saved to database: entry {entry_number}, value {value}")
    except Exception as e:
        print(f"Error saving to database: {e}")
        session.rollback()
    finally:
        session.close()

def get_all_entries():
    """Retrieve all entries"""
    session = Session()
    try:
        entries = session.query(UserEntry).all()
        return entries
    finally:
        session.close()
