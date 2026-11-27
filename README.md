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
# For 1st Task
sudo -u postgres psql
CREATE DATABASE conference_part1_db;
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db -f schema.sql
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db -f seed.sql
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db

sudo -u postgres psql
CREATE DATABASE conference_db;
source ~/venv/bin/activate
export DATABASE_URL="postgresql://postgres:123456@localhost:5432/conference_db"
python setup_db.py     # for Task 2, 1-2 parts
python queries.py     # for Task 2, 3-8 parts       #output will be copied to output.txt
python app.py   # Task 3 run web
```

## Schema

- users
- sessions 
- papers
- reviews. 

## Keys
- user_id
- author_id
- reviewer_id
- conference_id
- track_id
- session_id
- paper_id
- review_id

## Required checks
- check unique values, so they are unique
- check that primary and foreign keys are not null
- no self-reviews
- paper must be accepted, and its track and session must belong to the same conference

## Optional Business rules
- Every user has at least one role.
- Include author-only, reviewer-only, and users with both roles.
- Every paper has exactly one corresponding author.
- Coordinators and chairs belong to their conference's reviewer pool.
