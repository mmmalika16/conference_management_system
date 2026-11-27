from sqlalchemy import text
from db import engine


def run(conn, sql, params=None):
    result = conn.execute(text(sql), params or {})

    if result.returns_rows:
        print(" | ".join(result.keys()))

        for row in result:
            print(" | ".join(str(x) if x is not None else "None" for x in row))
    else:
        print(result.rowcount)


def task_3_1():
    print("3.1")

    params = {
        "email": "arman.armanov@example.com",
        "phone": "+77773414141"
    }

    with engine.connect() as conn:
        trans = conn.begin()

        run(conn, """
            SELECT * FROM app_user
            WHERE email = :email
        """, params)

        run(conn, """
            UPDATE app_user
            SET phone_number = :phone
            WHERE email = :email
        """, params)

        run(conn, """
            SELECT * FROM app_user
            WHERE email = :email
        """, params)

        trans.rollback()


def task_3_2():
    print("3.2")

    with engine.connect() as conn:
        trans = conn.begin()

        run(conn, """
            UPDATE conference
            SET review_deadline = review_deadline +
                CASE
                    WHEN city = 'Astana' THEN INTERVAL '7 days'
                    ELSE INTERVAL '3 days'
                END
        """)

        run(conn, """
            SELECT conference_id, acronym, city, review_deadline
            FROM conference
            ORDER BY conference_id
        """)

        trans.rollback()


def task_4_1():
    print("4.1")

    params = {"email": "amina.aminova@example.com"}

    with engine.connect() as conn:
        trans = conn.begin()

        run(conn, """
            SELECT p.paper_id, p.title, p.status
            FROM paper p
            JOIN paper_author pa ON pa.paper_id = p.paper_id
            JOIN app_user u ON u.user_id = pa.author_id
            WHERE pa.is_corresponding = TRUE
              AND u.email = :email
              AND p.status = 'withdrawn'
        """, params)

        run(conn, """
            DELETE FROM review
            WHERE paper_id IN (
                SELECT p.paper_id
                FROM paper p
                JOIN paper_author pa ON pa.paper_id = p.paper_id
                JOIN app_user u ON u.user_id = pa.author_id
                WHERE pa.is_corresponding = TRUE
                  AND u.email = :email
                  AND p.status = 'withdrawn'
            )
        """, params)

        run(conn, """
            DELETE FROM paper_version
            WHERE paper_id IN (
                SELECT p.paper_id
                FROM paper p
                JOIN paper_author pa ON pa.paper_id = p.paper_id
                JOIN app_user u ON u.user_id = pa.author_id
                WHERE pa.is_corresponding = TRUE
                  AND u.email = :email
                  AND p.status = 'withdrawn'
            )
        """, params)

        run(conn, """
            DELETE FROM paper_keyword
            WHERE paper_id IN (
                SELECT p.paper_id
                FROM paper p
                JOIN paper_author pa ON pa.paper_id = p.paper_id
                JOIN app_user u ON u.user_id = pa.author_id
                WHERE pa.is_corresponding = TRUE
                  AND u.email = :email
                  AND p.status = 'withdrawn'
            )
        """, params)

        run(conn, """
            DELETE FROM paper_author
            WHERE paper_id IN (
                SELECT p.paper_id
                FROM paper p
                JOIN paper_author pa ON pa.paper_id = p.paper_id
                JOIN app_user u ON u.user_id = pa.author_id
                WHERE pa.is_corresponding = TRUE
                  AND u.email = :email
                  AND p.status = 'withdrawn'
            )
        """, params)

        run(conn, """
            DELETE FROM paper
            WHERE status = 'withdrawn'
              AND paper_id IN (
                  SELECT pa.paper_id
                  FROM paper_author pa
                  JOIN app_user u ON u.user_id = pa.author_id
                  WHERE pa.is_corresponding = TRUE
                    AND u.email = :email
              )
        """, params)

        run(conn, """
            SELECT
                (SELECT COUNT(*) FROM paper) AS papers,
                (SELECT COUNT(*) FROM paper_author) AS authors,
                (SELECT COUNT(*) FROM paper_keyword) AS keywords,
                (SELECT COUNT(*) FROM paper_version) AS versions,
                (SELECT COUNT(*) FROM review) AS reviews
        """)

        trans.rollback()


def task_4_2():
    print("4.2")

    with engine.connect() as conn:
        trans = conn.begin()

        run(conn, """
            SELECT s.session_id, s.title, c.acronym
            FROM conference_session s
            JOIN conference c ON c.conference_id = s.conference_id
            WHERE c.city = 'Astana'
              AND NOT EXISTS (
                  SELECT 1
                  FROM paper p
                  WHERE p.session_id = s.session_id
              )
        """)

        run(conn, """
            DELETE FROM conference_session s
            WHERE s.conference_id IN (
                SELECT conference_id
                FROM conference
                WHERE city = 'Astana'
            )
            AND NOT EXISTS (
                SELECT 1
                FROM paper p
                WHERE p.session_id = s.session_id
            )
        """)

        run(conn, """
            SELECT conference_id, acronym
            FROM conference
            ORDER BY conference_id
        """)

        trans.rollback()


def task_5():
    with engine.connect() as conn:

        print("5.1")

        run(conn, """
            SELECT p.paper_id, p.title,
                   u.given_name || ' ' || u.surname AS author,
                   u.email, t.name AS track,
                   c.conference_id, c.acronym
            FROM paper p
            JOIN track t ON t.track_id = p.track_id
            JOIN conference c ON c.conference_id = t.conference_id
            JOIN paper_author pa ON pa.paper_id = p.paper_id
            JOIN app_user u ON u.user_id = pa.author_id
            WHERE p.status = 'accepted'
              AND pa.is_corresponding = TRUE
            ORDER BY p.paper_id
        """)

        print("5.2")

        run(conn, """
            SELECT paper_id, title
            FROM paper
            WHERE abstract ILIKE '%machine learning%'
            ORDER BY paper_id
        """)

        print("5.3")

        run(conn, """
            SELECT version_no, file_location, uploaded_at
            FROM paper_version
            WHERE paper_id = 1
            ORDER BY version_no DESC
        """)

        print("5.4")

        run(conn, """
            SELECT DISTINCT r.reviewer_id,
                   u.given_name || ' ' || u.surname AS full_name,
                   u.email
            FROM conference_reviewer cr
            JOIN reviewer r ON r.reviewer_id = cr.reviewer_id
            JOIN reviewer_expertise re ON re.reviewer_id = r.reviewer_id
            JOIN app_user u ON u.user_id = r.reviewer_id
            WHERE cr.conference_id = 1
              AND re.area_label = 'Databases'
              AND r.years_experience >= 3
            ORDER BY r.reviewer_id
        """)


def task_6():
    with engine.connect() as conn:

        print("6.1")

        run(conn, """
            SELECT t.track_id, t.name, t.conference_id,
                   COUNT(DISTINCT p.paper_id) AS paper_count,
                   COUNT(DISTINCT pa.author_id) AS author_count
            FROM track t
            LEFT JOIN paper p ON p.track_id = t.track_id
            LEFT JOIN paper_author pa ON pa.paper_id = p.paper_id
            GROUP BY t.track_id, t.name, t.conference_id
            ORDER BY t.track_id
        """)

        print("6.2")

        run(conn, """
            SELECT r.reviewer_id,
                   u.given_name || ' ' || u.surname AS full_name,
                   COUNT(rv.review_id) AS review_count,
                   ROUND(AVG(rv.overall_score), 2) AS avg_score
            FROM reviewer r
            JOIN app_user u ON u.user_id = r.reviewer_id
            LEFT JOIN review rv ON rv.reviewer_id = r.reviewer_id
            GROUP BY r.reviewer_id, u.given_name, u.surname
            ORDER BY r.reviewer_id
        """)

        print("6.3")

        run(conn, """
            SELECT c.conference_id, c.acronym,
                   COUNT(DISTINCT p.paper_id) AS total_papers,
                   COUNT(DISTINCT CASE
                       WHEN p.status = 'accepted' THEN p.paper_id
                   END) AS accepted_papers,
                   ROUND(AVG(rv.overall_score), 2) AS avg_score
            FROM conference c
            LEFT JOIN track t ON t.conference_id = c.conference_id
            LEFT JOIN paper p ON p.track_id = t.track_id
            LEFT JOIN review rv ON rv.paper_id = p.paper_id
            GROUP BY c.conference_id, c.acronym
            ORDER BY c.conference_id
        """)

        print("6.4")

        run(conn, """
            WITH review_counts AS (
                SELECT r.reviewer_id,
                       COUNT(rv.review_id) AS review_count
                FROM reviewer r
                LEFT JOIN review rv ON rv.reviewer_id = r.reviewer_id
                GROUP BY r.reviewer_id
            )
            SELECT rc.reviewer_id,
                   u.given_name || ' ' || u.surname AS full_name,
                   rc.review_count,
                   ROUND((SELECT AVG(review_count)
                          FROM review_counts), 2) AS overall_avg
            FROM review_counts rc
            JOIN app_user u ON u.user_id = rc.reviewer_id
            WHERE rc.review_count > (
                SELECT AVG(review_count)
                FROM review_counts
            )
            ORDER BY rc.reviewer_id
        """)


def task_7():
    print("7")

    with engine.connect() as conn:
        run(conn, """
            SELECT c.conference_id, c.acronym,
                   COUNT(CASE WHEN p.status = 'accepted' THEN 1 END)
                       AS accepted_count,
                   COUNT(CASE WHEN p.status = 'rejected' THEN 1 END)
                       AS rejected_count,
                   ROUND(
                       100.0 * COUNT(CASE WHEN p.status = 'accepted' THEN 1 END)
                       / NULLIF(
                           COUNT(CASE WHEN p.status IN ('accepted', 'rejected')
                                      THEN 1 END), 0
                       ), 2
                   ) AS acceptance_rate
            FROM conference c
            LEFT JOIN track t ON t.conference_id = c.conference_id
            LEFT JOIN paper p ON p.track_id = t.track_id
            GROUP BY c.conference_id, c.acronym
            ORDER BY c.conference_id
        """)


def task_8():
    print("8")

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE OR REPLACE VIEW accepted_paper_schedule AS
            SELECT p.paper_id, p.title AS paper_title,
                   c.conference_id, c.acronym,
                   t.name AS track_name,
                   s.session_id, s.title AS session_title,
                   s.session_date, s.start_time, s.end_time,
                   s.room_label,
                   ch.given_name || ' ' || ch.surname AS chair_name,
                   au.given_name || ' ' || au.surname AS corresponding_author,
                   au.email AS corresponding_email
            FROM paper p
            JOIN conference_session s ON s.session_id = p.session_id
            JOIN conference c ON c.conference_id = s.conference_id
            JOIN track t ON t.track_id = p.track_id
            JOIN app_user ch ON ch.user_id = s.chair_id
            JOIN paper_author pa ON pa.paper_id = p.paper_id
                                AND pa.is_corresponding = TRUE
            JOIN app_user au ON au.user_id = pa.author_id
            WHERE p.status = 'accepted'
        """))

    with engine.connect() as conn:
        run(conn, """
            SELECT *
            FROM accepted_paper_schedule
            ORDER BY conference_id, session_date,
                     start_time, session_id, paper_id
        """)


if __name__ == "__main__":
    task_3_1()
    task_3_2()
    task_4_1()
    task_4_2()
    task_5()
    task_6()
    task_7()
    task_8()