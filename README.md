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
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db -f schema.sql
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db -f seed.sql
PGPASSWORD=123456 psql -h localhost -U postgres -d conference_part1_db

sudo -u postgres psql
CREATE DATABASE conference_db;
source ~/venv/bin/activate
export DATABASE_URL="postgresql://postgres:123456@localhost:5432/conference_db"
python setup_db.py     # for the 2 Task, 1-2 tasks
python queries.py     
python app.py   
```

## Assignment validation rules

The application enforces these rules:

- A reviewer cannot review a paper they authored. This is checked when a review is created or changed and when an author is added to a paper.
- A paper with a session must be accepted, and its track and session must belong to the same conference. Paper status, track, and session changes are checked when saving a paper.
- Changing a session's conference is rejected when a scheduled paper would become invalid (the paper is not accepted or the paper track belongs to another conference).
- The chair of a session must belong to that conference's reviewer pool.
- A user must have at least one of the author or reviewer roles.
- A paper is prevented from having more than one corresponding author in the paper author form.
- Track coordinators and session chairs are stored as reviewers and checked against conference membership where the application exposes those entities.

Other optional data rules documented for the sample data include: every paper has at least one author and exactly one corresponding author, user roles are represented by the `author` and `reviewer` tables, and the conference reviewer pool is used for coordinators and chairs.

