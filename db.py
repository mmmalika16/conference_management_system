import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get( "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/conference_db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
