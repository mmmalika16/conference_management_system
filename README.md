# Conference Management System (CSCI 341, Assignment 3)

Research conference and paper review management system.
PostgreSQL database + Python/SQLAlchemy queries (Part 2) + Flask web app (Part 3).

## Software versions

| Software | Version |
|---|---|
| Python | 3.12 |
| PostgreSQL | 16 (local), hosted PostgreSQL for the deployed app |
| SQLAlchemy | 2.0.41 |
| psycopg2-binary | 2.9.10 |
| Flask | 3.1.1 |
| gunicorn | 23.0.0 (server on the hosting platform) |

## How to run

```bash
source ~/venv/bin/activate
export DATABASE_URL="postgresql://postgres:123456@localhost:5432/conference_db"
python setup_db.py     
python queries.py     
python app.py   
```

## Restoring the initial dataset

Run `python setup_db.py` again. `schema.sql` drops all tables and the view first,
so this always gives the original seed data.
Alternatively restore the dump: `psql -U postgres -d conference_db -f database/conference_dump.sql`
(on an empty database).

All updates and deletes in `queries.py` run inside a transaction that is rolled back,
so the seed data stays unchanged after running the queries.

## Schema, keys and references

| Table | Primary key | Foreign keys (on delete) | Other constraints |
|---|---|---|---|
| app_user | user_id | – | email UNIQUE |
| author | author_id | author_id → app_user (CASCADE) | |
| author_research_area | (author_id, area_label) | author_id → author (CASCADE) | |
| reviewer | reviewer_id | reviewer_id → app_user (CASCADE) | years_experience >= 0 |
| reviewer_expertise | (reviewer_id, area_label) | reviewer_id → reviewer (CASCADE) | |
| conference | conference_id | – | end_date >= start_date, review_deadline >= submission_deadline |
| conference_host | (conference_id, host_name) | conference_id → conference (CASCADE) | |
| conference_reviewer | (conference_id, reviewer_id) | conference_id → conference (CASCADE), reviewer_id → reviewer (RESTRICT) | |
| track | track_id | conference_id → conference (CASCADE), coordinator_id → reviewer (RESTRICT) | |
| conference_session | session_id | conference_id → conference (CASCADE), chair_id → reviewer (RESTRICT) | end_time > start_time |
| paper | paper_id | track_id → track (RESTRICT), session_id → conference_session (SET NULL) | status IN (submitted, under review, accepted, rejected, withdrawn) |
| paper_keyword | (paper_id, keyword) | paper_id → paper (CASCADE) | |
| paper_author | (paper_id, author_id) | paper_id → paper (CASCADE), author_id → author (RESTRICT) | UNIQUE (paper_id, author_position), author_position >= 1 |
| paper_version | (paper_id, version_no) | paper_id → paper (CASCADE) | version_no >= 1 |
| review | review_id | paper_id → paper (CASCADE), reviewer_id → reviewer (RESTRICT) | UNIQUE (paper_id, reviewer_id), overall_score 1–5, recommendation IN (accept, reject) |

Deletion actions:
* Deleting a paper deletes its versions, authorship, keywords and reviews (CASCADE).
* Deleting a session keeps its papers; their `session_id` becomes NULL.
* Deleting a conference deletes its hosts, reviewer pool rows, tracks and sessions,
  but never users or reviewers. It is rejected while its tracks still have papers.
* Deleting a user is rejected (RESTRICT) while the user is still referenced as a paper author,
  reviewer of a review, pool member, coordinator or chair. The error is shown in the web app.

Multivalued attributes (research areas, expertise, hosts, keywords, authors) are separate tables.
In the web app they are typed as comma-separated text, but each value is stored as its own row.

## Required application checks (in `app.py`)

1. **No self-reviews.** `check_not_self_review()` runs when a review is created or edited.
   When an author is added to a paper, `paper_author_add()` rejects the author if they already reviewed that paper.
2. **Valid session assignments.** `check_session_assignment()` runs every time a paper is saved
   (so it covers assigning a session and changing status or track): a paper with a session must be
   `accepted` and its track must be in the same conference as the session. Editing a session to move it
   to another conference is rejected while it has papers from the old conference.

Invalid changes are rejected, the transaction is rolled back and the error message is shown on the page.

## Optional business rules

| Rule | Holds in sample data | Enforced by app |
|---|---|---|
| Every user is an author, a reviewer, or both | yes | yes (user form) |
| Exactly one corresponding author per paper | yes | at most one is enforced when adding authors |
| Session chair is in the conference reviewer pool | yes | yes (session form) |
| Track coordinator is in the conference reviewer pool | yes | no (tracks are read-only seed data) |
| Reviewer of a paper is in the conference reviewer pool | yes | no |
| Every paper has at least one author and one version | yes | no (added on the paper page after creating the paper) |
| Every conference has at least one host | yes | no (read-only seed data) |

## Design assumptions

* The current version of a paper is the one with the highest `version_no`; gaps are allowed.
* Only completed reviews are stored.
* Conferences, tracks, hosts, reviewer pools and labels are read-only seed data used in drop-down lists.
* No authentication and no real file upload: a version stores a file location string.

## Query parameter values (queries.py)

| Task | Parameters |
|---|---|
| 3.1 | email = arman.armanov@example.com, phone = +77773414141 |
| 3.2 | city = Astana (+7 days), other cities +3 days |
| 4.1 | email = amina.aminova@example.com (deletes withdrawn papers 6 and 7) |
| 4.2 | city = Astana (deletes empty session 2) |
| 5.2 | pattern = %machine learning% (ILIKE) |
| 5.3 | paper_id = 1 (has versions 2 and 1) |
| 5.4 | conference_id = 1, area = Databases, years >= 3 (returns reviewer 5) |

## Sample data coverage

* 10 users: author only (2, 4, 8), reviewer only (1, 5, 7, 9, 10), both (3, 6).
* All five paper statuses; papers with several authors; paper 1 has two versions.
* Empty track: track 2 (AI). Conference with no papers: conference 2 (CAI, Almaty).
* Reviewers with no reviews: 3, 6, 9, 10. Review counts vary (4, 4, 3, 0...) for task 6.4.
* Accepted paper with a session (paper 1) and without (paper 2).
* Amina Aminova is corresponding author of withdrawn papers 6 and 7.
* Empty session in an Astana conference: session 2. Conferences in Astana and Almaty.

## Deployment

The web app runs on Render (Web Service, start command `gunicorn app:app`) and uses a hosted
PostgreSQL database (Neon). The database URL is given to the app with the `DATABASE_URL`
environment variable. The URL is in `links.txt`.
