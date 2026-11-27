import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from db import engine

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

STATUSES = ["submitted", "under review", "accepted", "rejected", "withdrawn"]


def query(sql, params=None):
    with engine.connect() as conn:
        return conn.execute(text(sql), params or {}).mappings().all()

def query_one(sql, params=None):
    rows = query(sql, params)
    return rows[0] if rows else None

def error_text(e):
    return str(getattr(e, "orig", None) or e)

def split_list(value):
    return [x.strip() for x in value.split(",") if x.strip()]


def empty_to_none(value):
    return value if value else None


def check_session_assignment(conn, track_id, status, session_id):
    if not session_id:
        return
    if status != "accepted":
        raise ValueError("Only accepted papers can be assigned to a session.")
    track = conn.execute(text("SELECT name, conference_id FROM track WHERE track_id = :t"),
                         {"t": track_id}).mappings().one()
    session = conn.execute(text("SELECT title, conference_id FROM conference_session WHERE session_id = :s"),
                           {"s": session_id}).mappings().one()
    if track["conference_id"] != session["conference_id"]:
        raise ValueError("The paper's track and the session belong to different conferences.")
    if track["name"].strip().lower() != session["title"].strip().lower():
        raise ValueError(
            f"Track '{track['name']}' does not match session '{session['title']}'."
        )


def check_not_self_review(conn, paper_id, reviewer_id):
    found = conn.execute(text("SELECT 1 FROM paper_author WHERE paper_id = :p AND author_id = :r"),
                         {"p": paper_id, "r": reviewer_id}).first()
    if found:
        raise ValueError("Self-review is not allowed: this reviewer is an author of the paper.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    rows = query("""
        SELECT u.*,
               EXISTS (SELECT 1 FROM author a WHERE a.author_id = u.user_id) AS is_author,
               EXISTS (SELECT 1 FROM reviewer r WHERE r.reviewer_id = u.user_id) AS is_reviewer
        FROM app_user u ORDER BY u.user_id""")
    return render_template("users.html", users=rows)


@app.route("/users/new", methods=["GET", "POST"])
@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def user_form(user_id=None):
    if request.method == "POST":
        f = request.form
        is_author = "is_author" in f
        is_reviewer = "is_reviewer" in f
        try:
            if not valid_email(f["email"]):
                raise ValueError("Please enter a valid email address.")
            if not is_author and not is_reviewer:
                raise ValueError("A user must be an author, a reviewer, or both.")
            with engine.begin() as conn:
                params = {
                    "given_name": f["given_name"], "surname": f["surname"], "email": f["email"],
                    "affiliation": f["affiliation"], "country": f["country"],
                    "phone": empty_to_none(f["phone_number"]),
                }
                if user_id is None:
                    user_id = conn.execute(text("""
                        INSERT INTO app_user (given_name, surname, email, affiliation, country, phone_number)
                        VALUES (:given_name, :surname, :email, :affiliation, :country, :phone)
                        RETURNING user_id"""), params).scalar()
                else:
                    params["id"] = user_id
                    conn.execute(text("""
                        UPDATE app_user SET given_name = :given_name, surname = :surname, email = :email,
                               affiliation = :affiliation, country = :country, phone_number = :phone
                        WHERE user_id = :id"""), params)

                if is_author:
                    conn.execute(text("""
                        INSERT INTO author (author_id, orcid) VALUES (:id, :orcid)
                        ON CONFLICT (author_id) DO UPDATE SET orcid = :orcid"""),
                                 {"id": user_id, "orcid": empty_to_none(f["orcid"])})
                    conn.execute(text("DELETE FROM author_research_area WHERE author_id = :id"), {"id": user_id})
                    for area in split_list(f["research_areas"]):
                        conn.execute(text("INSERT INTO author_research_area VALUES (:id, :area)"),
                                     {"id": user_id, "area": area})
                else:
                    conn.execute(text("DELETE FROM author WHERE author_id = :id"), {"id": user_id})

                if is_reviewer:
                    conn.execute(text("""
                        INSERT INTO reviewer (reviewer_id, years_experience) VALUES (:id, :years)
                        ON CONFLICT (reviewer_id) DO UPDATE SET years_experience = :years"""),
                                 {"id": user_id, "years": int(f["years_experience"] or 0)})
                    conn.execute(text("DELETE FROM reviewer_expertise WHERE reviewer_id = :id"), {"id": user_id})
                    for area in split_list(f["expertise"]):
                        conn.execute(text("INSERT INTO reviewer_expertise VALUES (:id, :area)"),
                                     {"id": user_id, "area": area})
                else:
                    conn.execute(text("DELETE FROM reviewer WHERE reviewer_id = :id"), {"id": user_id})
            flash("User saved.")
            return redirect(url_for("users"))
        except Exception as e:
            flash("Error: " + error_text(e))
            invalid_fields = ["email"] if not valid_email(f["email"]) else []
            form_data = preserve_form(f, invalid_fields)
            # Load the same options/metadata used by the GET view.
            user = form_data
            author = {"orcid": form_data.get("orcid", "")} if is_author else None
            reviewer = {"years_experience": form_data.get("years_experience", 0)} if is_reviewer else None
            areas = form_data.get("research_areas", "")
            expertise = form_data.get("expertise", "")
            return render_template("user_form.html", user=user, author=author, reviewer=reviewer,
                                   areas=areas, expertise=expertise)

    user, author, reviewer, areas, expertise = None, None, None, "", ""
    if user_id is not None:
        user = query_one("SELECT * FROM app_user WHERE user_id = :id", {"id": user_id})
        author = query_one("SELECT * FROM author WHERE author_id = :id", {"id": user_id})
        reviewer = query_one("SELECT * FROM reviewer WHERE reviewer_id = :id", {"id": user_id})
        areas = ", ".join(r["area_label"] for r in
                          query("SELECT area_label FROM author_research_area WHERE author_id = :id", {"id": user_id}))
        expertise = ", ".join(r["area_label"] for r in
                              query("SELECT area_label FROM reviewer_expertise WHERE reviewer_id = :id", {"id": user_id}))
    return render_template("user_form.html", user=user, author=author, reviewer=reviewer,
                           areas=areas, expertise=expertise)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM app_user WHERE user_id = :id"), {"id": user_id})
        flash("User deleted.")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("users"))


@app.route("/papers")
def papers():
    rows = query("""
        SELECT p.paper_id, p.title, p.status, t.name AS track_name, c.acronym, s.title AS session_title
        FROM paper p
        JOIN track t ON t.track_id = p.track_id
        JOIN conference c ON c.conference_id = t.conference_id
        LEFT JOIN conference_session s ON s.session_id = p.session_id
        ORDER BY p.paper_id""")
    return render_template("papers.html", papers=rows)


@app.route("/papers/new", methods=["GET", "POST"])
@app.route("/papers/<int:paper_id>/edit", methods=["GET", "POST"])
def paper_form(paper_id=None):
    if request.method == "POST":
        f = request.form
        try:
            with engine.begin() as conn:
                params = {
                    "track_id": int(f["track_id"]), "title": f["title"], "abstract": f["abstract"],
                    "submission_date": f["submission_date"], "status": f["status"],
                    "session_id": int(f["session_id"]) if f["session_id"] else None,
                }
                check_session_assignment(conn, params["track_id"], params["status"], params["session_id"])
                if paper_id is None:
                    paper_id = conn.execute(text("""
                        INSERT INTO paper (track_id, title, abstract, submission_date, status, session_id)
                        VALUES (:track_id, :title, :abstract, :submission_date, :status, :session_id)
                        RETURNING paper_id"""), params).scalar()
                else:
                    params["id"] = paper_id
                    conn.execute(text("""
                        UPDATE paper SET track_id = :track_id, title = :title, abstract = :abstract,
                               submission_date = :submission_date, status = :status, session_id = :session_id
                        WHERE paper_id = :id"""), params)
                conn.execute(text("DELETE FROM paper_keyword WHERE paper_id = :id"), {"id": paper_id})
                for kw in split_list(f["keywords"]):
                    conn.execute(text("INSERT INTO paper_keyword VALUES (:id, :kw)"), {"id": paper_id, "kw": kw})
            flash("Paper saved. Add authors and versions below.")
            return redirect(url_for("paper_detail", paper_id=paper_id))
        except Exception as e:
            flash("Error: " + error_text(e))
            submitted = preserve_form(f)
            tracks = query("""SELECT t.track_id, t.name, c.acronym FROM track t
                              JOIN conference c ON c.conference_id = t.conference_id ORDER BY t.track_id""")
            sessions = query("""SELECT s.session_id, s.title, c.acronym FROM conference_session s
                                JOIN conference c ON c.conference_id = s.conference_id ORDER BY s.session_id""")
            paper = submitted
            return render_template("paper_form.html", paper=paper,
                                   submitted=submitted, keywords=submitted.get("keywords", ""),
                                   tracks=tracks, sessions=sessions, statuses=STATUSES)

    paper, keywords = None, ""
    if paper_id is not None:
        paper = query_one("SELECT * FROM paper WHERE paper_id = :id", {"id": paper_id})
        keywords = ", ".join(r["keyword"] for r in
                             query("SELECT keyword FROM paper_keyword WHERE paper_id = :id", {"id": paper_id}))
    tracks = query("""SELECT t.track_id, t.name, c.acronym FROM track t
                      JOIN conference c ON c.conference_id = t.conference_id ORDER BY t.track_id""")
    sessions = query("""SELECT s.session_id, s.title, c.acronym FROM conference_session s
                        JOIN conference c ON c.conference_id = s.conference_id ORDER BY s.session_id""")
    return render_template("paper_form.html", paper=paper, keywords=keywords,
                           tracks=tracks, sessions=sessions, statuses=STATUSES)


@app.route("/papers/<int:paper_id>")
def paper_detail(paper_id):
    paper = query_one("""
        SELECT p.*, t.name AS track_name, c.acronym, s.title AS session_title
        FROM paper p
        JOIN track t ON t.track_id = p.track_id
        JOIN conference c ON c.conference_id = t.conference_id
        LEFT JOIN conference_session s ON s.session_id = p.session_id
        WHERE p.paper_id = :id""", {"id": paper_id})
    if paper is None:
        flash("Paper not found.")
        return redirect(url_for("papers"))
    keywords = query("SELECT keyword FROM paper_keyword WHERE paper_id = :id ORDER BY keyword", {"id": paper_id})
    authors = query("""
        SELECT pa.author_id, pa.author_position, pa.is_corresponding, u.given_name, u.surname
        FROM paper_author pa JOIN app_user u ON u.user_id = pa.author_id
        WHERE pa.paper_id = :id ORDER BY pa.author_position""", {"id": paper_id})
    versions = query("SELECT * FROM paper_version WHERE paper_id = :id ORDER BY version_no DESC", {"id": paper_id})
    reviews = query("""
        SELECT rv.review_id, rv.overall_score, rv.recommendation, u.given_name, u.surname
        FROM review rv JOIN app_user u ON u.user_id = rv.reviewer_id
        WHERE rv.paper_id = :id ORDER BY rv.review_id""", {"id": paper_id})
    all_authors = query("""SELECT a.author_id, u.given_name, u.surname FROM author a
                           JOIN app_user u ON u.user_id = a.author_id ORDER BY a.author_id""")
    next_version = (versions[0]["version_no"] + 1) if versions else 1
    return render_template("paper_detail.html", paper=paper, keywords=keywords, authors=authors,
                           versions=versions, reviews=reviews, all_authors=all_authors,
                           next_version=next_version)


@app.route("/papers/<int:paper_id>/delete", methods=["POST"])
def paper_delete(paper_id):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM paper WHERE paper_id = :id"), {"id": paper_id})
        flash("Paper deleted (with its authorship, keywords, versions and reviews).")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("papers"))


@app.route("/papers/<int:paper_id>/authors/add", methods=["POST"])
def paper_author_add(paper_id):
    f = request.form
    author_id = int(f["author_id"])
    is_corresponding = "is_corresponding" in f
    try:
        with engine.begin() as conn:
            reviewed = conn.execute(text("SELECT 1 FROM review WHERE paper_id = :p AND reviewer_id = :a"),
                                    {"p": paper_id, "a": author_id}).first()
            if reviewed:
                raise ValueError("This person already reviewed the paper, so they cannot be its author (self-review).")
            if is_corresponding:
                other = conn.execute(text("""SELECT 1 FROM paper_author
                                             WHERE paper_id = :p AND is_corresponding = TRUE"""),
                                     {"p": paper_id}).first()
                if other:
                    raise ValueError("This paper already has a corresponding author.")
            conn.execute(text("""
                INSERT INTO paper_author (paper_id, author_id, author_position, is_corresponding)
                VALUES (:p, :a, :pos, :corr)"""),
                         {"p": paper_id, "a": author_id, "pos": int(f["author_position"]), "corr": is_corresponding})
        flash("Author added.")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("paper_detail", paper_id=paper_id))


@app.route("/papers/<int:paper_id>/authors/<int:author_id>/delete", methods=["POST"])
def paper_author_delete(paper_id, author_id):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM paper_author WHERE paper_id = :p AND author_id = :a"),
                         {"p": paper_id, "a": author_id})
        flash("Author removed.")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("paper_detail", paper_id=paper_id))


@app.route("/papers/<int:paper_id>/versions/add", methods=["POST"])
def paper_version_add(paper_id):
    f = request.form
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO paper_version (paper_id, version_no, file_location, uploaded_at, change_note)
                VALUES (:p, :v, :loc, NOW(), :note)"""),
                         {"p": paper_id, "v": int(f["version_no"]), "loc": f["file_location"],
                          "note": empty_to_none(f["change_note"])})
        flash("Version added.")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("paper_detail", paper_id=paper_id))


@app.route("/papers/<int:paper_id>/versions/<int:version_no>/delete", methods=["POST"])
def paper_version_delete(paper_id, version_no):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM paper_version WHERE paper_id = :p AND version_no = :v"),
                         {"p": paper_id, "v": version_no})
        flash("Version deleted.")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("paper_detail", paper_id=paper_id))


@app.route("/reviews")
def reviews():
    rows = query("""
        SELECT rv.*, p.title, u.given_name, u.surname
        FROM review rv
        JOIN paper p ON p.paper_id = rv.paper_id
        JOIN app_user u ON u.user_id = rv.reviewer_id
        ORDER BY rv.review_id""")
    return render_template("reviews.html", reviews=rows)


@app.route("/reviews/new", methods=["GET", "POST"])
@app.route("/reviews/<int:review_id>/edit", methods=["GET", "POST"])
def review_form(review_id=None):
    if request.method == "POST":
        f = request.form
        try:
            with engine.begin() as conn:
                params = {
                    "paper_id": int(f["paper_id"]), "reviewer_id": int(f["reviewer_id"]),
                    "score": int(f["overall_score"]), "rec": f["recommendation"],
                    "comments": f["comments_for_authors"],
                    "confidential": empty_to_none(f["confidential_comments"]),
                    "date": f["review_submission_date"],
                }
                check_not_self_review(conn, params["paper_id"], params["reviewer_id"])
                if review_id is None:
                    conn.execute(text("""
                        INSERT INTO review (paper_id, reviewer_id, overall_score, recommendation,
                                            comments_for_authors, confidential_comments, review_submission_date)
                        VALUES (:paper_id, :reviewer_id, :score, :rec, :comments, :confidential, :date)"""), params)
                else:
                    params["id"] = review_id
                    conn.execute(text("""
                        UPDATE review SET paper_id = :paper_id, reviewer_id = :reviewer_id,
                               overall_score = :score, recommendation = :rec,
                               comments_for_authors = :comments, confidential_comments = :confidential,
                               review_submission_date = :date
                        WHERE review_id = :id"""), params)
            flash("Review saved.")
            return redirect(url_for("reviews"))
        except Exception as e:
            flash("Error: " + error_text(e))
            submitted = preserve_form(f)
            review = submitted
            papers_list = query("SELECT paper_id, title FROM paper ORDER BY paper_id")
            reviewers = query("""SELECT r.reviewer_id, u.given_name, u.surname FROM reviewer r
                                 JOIN app_user u ON u.user_id = r.reviewer_id ORDER BY r.reviewer_id""")
            return render_template("review_form.html", review=review, submitted=submitted,
                                   papers=papers_list, reviewers=reviewers)

    review = None
    if review_id is not None:
        review = query_one("SELECT * FROM review WHERE review_id = :id", {"id": review_id})
    papers_list = query("SELECT paper_id, title FROM paper ORDER BY paper_id")
    reviewers = query("""SELECT r.reviewer_id, u.given_name, u.surname FROM reviewer r
                         JOIN app_user u ON u.user_id = r.reviewer_id ORDER BY r.reviewer_id""")
    return render_template("review_form.html", review=review, papers=papers_list, reviewers=reviewers)


@app.route("/reviews/<int:review_id>/delete", methods=["POST"])
def review_delete(review_id):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM review WHERE review_id = :id"), {"id": review_id})
        flash("Review deleted.")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("reviews"))


@app.route("/sessions")
def sessions():
    rows = query("""
        SELECT s.*, c.acronym, u.given_name, u.surname,
               (SELECT COUNT(*) FROM paper p WHERE p.session_id = s.session_id) AS paper_count
        FROM conference_session s
        JOIN conference c ON c.conference_id = s.conference_id
        JOIN app_user u ON u.user_id = s.chair_id
        ORDER BY s.session_id""")
    return render_template("sessions.html", sessions=rows)


@app.route("/sessions/new", methods=["GET", "POST"])
@app.route("/sessions/<int:session_id>/edit", methods=["GET", "POST"])
def session_form(session_id=None):
    if request.method == "POST":
        f = request.form
        try:
            with engine.begin() as conn:
                params = {
                    "conf": int(f["conference_id"]), "title": f["title"], "date": f["session_date"],
                    "start": f["start_time"], "end": f["end_time"], "room": f["room_label"],
                    "chair": int(f["chair_id"]),
                }
                in_pool = conn.execute(text("""SELECT 1 FROM conference_reviewer
                                               WHERE conference_id = :conf AND reviewer_id = :chair"""),
                                       params).first()
                if not in_pool:
                    raise ValueError("The chair must be in this conference's reviewer pool.")
                if session_id is None:
                    conn.execute(text("""
                        INSERT INTO conference_session (conference_id, title, session_date, start_time,
                                                        end_time, room_label, chair_id)
                        VALUES (:conf, :title, :date, :start, :end, :room, :chair)"""), params)
                else:
                    bad = conn.execute(text("""
                        SELECT COUNT(*) FROM paper p JOIN track t ON t.track_id = p.track_id
                        WHERE p.session_id = :id AND t.conference_id <> :conf"""),
                                       {"id": session_id, "conf": params["conf"]}).scalar()
                    if bad > 0:
                        raise ValueError("Papers assigned to this session belong to another conference. "
                                         "Remove them from the session first.")
                    params["id"] = session_id
                    conn.execute(text("""
                        UPDATE conference_session SET conference_id = :conf, title = :title,
                               session_date = :date, start_time = :start, end_time = :end,
                               room_label = :room, chair_id = :chair
                        WHERE session_id = :id"""), params)
            flash("Session saved.")
            return redirect(url_for("sessions"))
        except Exception as e:
            flash("Error: " + error_text(e))
            submitted = preserve_form(f)
            session = submitted
            conferences = query("SELECT conference_id, acronym, city FROM conference ORDER BY conference_id")
            reviewers = query("""SELECT r.reviewer_id, u.given_name, u.surname FROM reviewer r
                                 JOIN app_user u ON u.user_id = r.reviewer_id ORDER BY r.reviewer_id""")
            return render_template("session_form.html", session=session, submitted=submitted,
                                   conferences=conferences, reviewers=reviewers)

    session = None
    if session_id is not None:
        session = query_one("SELECT * FROM conference_session WHERE session_id = :id", {"id": session_id})
    conferences = query("SELECT conference_id, acronym, city FROM conference ORDER BY conference_id")
    reviewers = query("""SELECT r.reviewer_id, u.given_name, u.surname FROM reviewer r
                         JOIN app_user u ON u.user_id = r.reviewer_id ORDER BY r.reviewer_id""")
    return render_template("session_form.html", session=session, conferences=conferences, reviewers=reviewers)


@app.route("/sessions/<int:session_id>/delete", methods=["POST"])
def session_delete(session_id):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM conference_session WHERE session_id = :id"), {"id": session_id})
        flash("Session deleted (its papers are now unscheduled).")
    except Exception as e:
        flash("Error: " + error_text(e))
    return redirect(url_for("sessions"))


def preserve_form(form, invalid_fields=None):
    data = form.to_dict()
    for field in invalid_fields or ():
        data[field] = ""
    return data


def valid_email(email):
    email = email.strip()
    return "@" in email and "." in email.rsplit("@", 1)[-1]


if __name__ == "__main__":
    app.run(debug=True)
