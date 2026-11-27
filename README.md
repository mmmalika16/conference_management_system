# Conference Management System (CSCI 341, Assignment 3)

## Software versions

Python - 3.12
PostgreSQL - 16 local
SQLAlchemy - 2.0.41 
psycopg2-binary - 2.9.10
Flask - 3.1.1 
gunicorn - 23.0.0

## How to run

```bash
sudo -u postgres psql
CREATE DATABASE conference_part1_db;
\q
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db -f schema.sql
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db -f seed.sql
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db
\dt

sudo -u postgres psql

CREATE DATABASE conference_db;
\q
source ~/venv/bin/activate
export DATABASE_URL="postgresql://postgres:123456@localhost:5432/conference_db"
python setup_db.py     
python queries.py     
python app.py   
```

