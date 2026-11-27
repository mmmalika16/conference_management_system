from sqlalchemy import text
from db import engine

TABLES = [
    "app_user", "author", "author_research_area", "reviewer", "reviewer_expertise",
    "conference", "conference_host", "conference_reviewer", "track",
    "conference_session", "paper", "paper_keyword", "paper_author",
    "paper_version", "review",
]

ID_COLUMNS = [
    ("app_user", "user_id"), ("conference", "conference_id"), ("track", "track_id"),
    ("conference_session", "session_id"), ("paper", "paper_id"), ("review", "review_id"),
]


def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    schema_sql = read_file("database/schema.sql")
    seed_sql = read_file("database/seed.sql")

    with engine.begin() as conn:
        print("1. Create statements")
        print(schema_sql)
        conn.exec_driver_sql(schema_sql)
        print("Tables created.\n")

        print("2. Update statements")
        print(seed_sql)
        conn.exec_driver_sql(seed_sql)

        for table, col in ID_COLUMNS:
            conn.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', '{col}'), "
                f"(SELECT MAX({col}) FROM {table}))"
            ))

        print("\nRow count of every table:")
        for table in TABLES:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  {table:22} {count}")

if __name__ == "__main__":
    main()
