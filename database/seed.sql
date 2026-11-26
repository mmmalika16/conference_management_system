INSERT INTO app_user (user_id, given_name, surname, email, affiliation, country, phone_number)
VALUES
(1, 'Arman', 'Armanov', 'arman.armanov@example.com', 'NU', 'Kazakhstan', '+7 777 123 4567'),
(2, 'Amina', 'Aminova', 'amina.aminova@example.com', 'NU', 'Kazakhstan', '+7 777 123 4568'),
(3, 'Iliyas', 'Zharylgasin', 'iliyasz@example.com', 'NU', 'Kazakhstan', '+7 777 123 4569'),
(4, 'Malika', 'Meiramova', 'malikameiramova@example.com', 'NU', 'Kazakhstan', '+7 777 123 4560'),
(5, 'Dias', 'Dias', 'diad.dias@example.com', 'NU', 'Kazakhstan', '+7 777 123 4561'),
(6, 'Aibar', 'Aibar', 'aibar.aibar@example.com', 'NU', 'Kazakhstan', '+7 777 123 4562'),
(7, 'ALikhan', 'ALikhan', 'alikhan.alikhan@example.com', 'NU', 'Kazakhstan', '+7 777 123 4563'),
(8, 'Daniyar', 'Daniyar', 'daniyar.daniyar@example.com', 'NU', 'Kazakhstan', '+7 777 123 4564'),
(9, 'Lila', 'Lila', 'lila.lila@example.com', 'NU', 'Kazakhstan', '+7 777 123 4565'),
(10, 'Zarina', 'Zarina', 'zarina.zarina@example.com', 'NU', 'Kazakhstan', '+7 777 123 4566');

INSERT INTO author (author_id, orcid)
VALUES
(2, NULL),
(3, '0000-0000-0000-0001'),
(4, '0000-0000-0000-0002'),
(6, '0000-0000-0000-0003'),
(8, '0000-0000-0000-0004');

INSERT INTO author_research_area (author_id, area_label)
VALUES
(2, 'CS'),
(3, 'ML'),
(4, 'AI'),
(6, 'ROBT'),
(8, 'DB');

INSERT INTO reviewer (reviewer_id, years_experience)
VALUES
(1, 3),
(3, 4),
(5, 5),
(6, 6),
(7, 7),
(9, 8),
(10, 0);

INSERT INTO reviewer_expertise (reviewer_id, area_label)
VALUES
(1, 'CS'),
(3, 'ML'),
(5, 'Databases'),
(6, 'ROBT'),
(7, 'AI'),
(9, 'DB'),
(10, 'AI');

INSERT INTO conference (conference_id, name, acronym, description, city, country, start_date, end_date, submission_deadline, review_deadline)
VALUES
(1, 'Conference of Computer Science', 'CCS', 'Conference of CS', 'Astana', 'Kazakhstan', '2027-04-10', '2027-04-12', '2027-02-01', '2027-03-01'),
(2, 'Conference on Artificial Intelligence', 'CAI', 'Conference of AI', 'Almaty', 'Kazakhstan', '2027-05-10', '2027-05-12', '2027-03-01', '2027-04-01');

INSERT INTO conference_host (conference_id, host_name)
VALUES
(1, 'NU'),
(2, 'KBTU');

INSERT INTO conference_reviewer (conference_id, reviewer_id)
VALUES
(1, 1),
(1, 5),
(1, 6),
(1, 7),
(2, 3),
(2, 6);

INSERT INTO track (track_id, conference_id, name, description, research_area, coordinator_id)
VALUES
(1, 1, 'DS', 'Data Science', 'CS', 5),
(2, 1, 'AI', 'Artificial Intelligence', 'AI', 1);

INSERT INTO conference_session (session_id, conference_id, title, session_date, start_time, end_time, room_label, chair_id)
VALUES
(1, 1, 'ML', '2027-04-10', '09:00', '10:30', 'A', 7),
(2, 1, 'DS', '2027-04-11', '11:00', '12:30', 'B', 5);

INSERT INTO paper (paper_id, track_id, title, abstract, submission_date, status, session_id)
VALUES
(1, 1, 'ML for Health', 'This paper studies machine learning methods for healthcare.', '2027-01-10', 'accepted', 1),
(2, 1, 'ML for Security', 'This paper studies machine learning methods for security.', '2027-01-11', 'accepted', NULL),
(3, 1, 'ML for Sport', 'This paper studies machine learning methods for sport.', '2027-01-12', 'submitted', NULL),
(4, 1, 'ML for Education', 'This paper studies machine learning methods for education.', '2027-01-13', 'under review', NULL),
(5, 1, 'ML for Environment', 'This paper studies machine learning methods for environment.', '2027-01-14', 'rejected', NULL),
(6, 1, 'ML for Finance', 'This paper studies machine learning methods for finance.', '2027-01-15', 'withdrawn', NULL),
(7, 1, 'ML for Marketing', 'This paper studies machine learning methods for marketing.', '2027-01-16', 'withdrawn', NULL),
(8, 1, 'ML for Healthcare', 'This paper studies machine learning methods for healthcare.', '2027-01-17', 'submitted', NULL),
(9, 1, 'ML for Transportation', 'This paper studies machine learning methods for transportation.', '2027-01-18', 'under review', NULL),
(10, 1, 'ML for Agriculture', 'This paper studies machine learning methods for agriculture.', '2027-01-19', 'rejected', NULL);

INSERT INTO paper_keyword (paper_id, keyword)
VALUES
(1, 'machine learning'),
(1, 'healthcare'),
(2, 'machine learning'),
(2, 'security'),
(3, 'machine learning'),
(3, 'sport'),
(4, 'machine learning'),
(4, 'education'),
(5, 'machine learning'),
(5, 'environment'),
(6, 'machine learning'),
(6, 'finance'),
(7, 'machine learning'),
(7, 'marketing'),
(8, 'machine learning'),
(8, 'healthcare'),
(9, 'machine learning'),
(9, 'transportation'),
(10, 'machine learning'),
(10, 'agriculture');

INSERT INTO paper_author (paper_id, author_id, author_position, is_corresponding)
VALUES
(1, 2, 1, TRUE),
(1, 4, 2, FALSE),
(2, 3, 1, TRUE),
(2, 8, 2, FALSE),
(3, 4, 1, TRUE),
(3, 8, 2, FALSE),
(4, 2, 1, TRUE),
(5, 4, 1, TRUE),
(6, 2, 1, TRUE),
(6, 8, 2, FALSE),
(7, 2, 1, TRUE),
(7, 4, 2, FALSE),
(8, 2, 1, TRUE),
(9, 8, 1, TRUE),
(10, 4, 1, TRUE);

INSERT INTO paper_version (paper_id, version_no, file_location, uploaded_at, change_note)
VALUES
(1, 1, 'paper_version/p1_v1.pdf', '2027-01-10 10:00:00', 'Initial version'),
(1, 2, 'paper_version/p1_v2.pdf', '2027-01-12 12:00:00', 'Updated version'),
(2, 1, 'paper_version/p2_v1.pdf', '2027-01-11 10:00:00', 'Initial version'),
(3, 1, 'paper_version/p3_v1.pdf', '2027-01-12 10:00:00', 'Initial version'),
(4, 1, 'paper_version/p4_v1.pdf', '2027-01-13 10:00:00', 'Initial version'),
(5, 1, 'paper_version/p5_v1.pdf', '2027-01-14 10:00:00', 'Initial version'),
(6, 1, 'paper_version/p6_v1.pdf', '2027-01-15 10:00:00', 'Initial version'),
(7, 1, 'paper_version/p7_v1.pdf', '2027-01-16 10:00:00', 'Initial version'),
(8, 1, 'paper_version/p8_v1.pdf', '2027-01-17 10:00:00', 'Initial version'),
(9, 1, 'paper_version/p9_v1.pdf', '2027-01-18 10:00:00', 'Initial version'),
(10, 1, 'paper_version/p10_v1.pdf', '2027-01-19 10:00:00', 'Initial version');

INSERT INTO review (review_id, paper_id, reviewer_id, overall_score, recommendation, comments_for_authors, confidential_comments, review_submission_date)
VALUES
(1, 1, 5, 5, 'accept', 'Good', 'Strong contribution', '2027-02-01'),
(2, 1, 7, 4, 'accept', 'Interesting', 'Minor Issues', '2027-02-02'),
(3, 2, 1, 4, 'accept', 'Good', 'Good quality', '2027-02-03'),
(4, 2, 5, 3, 'accept', 'Interesting', 'Reccomend acceptance', '2027-02-04'),
(5, 3, 1, 3, 'reject', 'Good', 'NO major issues', '2027-02-05'),
(6, 3, 7, 4, 'accept', 'Interesting', 'Some weaknesses', '2027-02-06'),
(7, 4, 1, 3, 'reject', 'Good', 'Insufficient', '2027-02-07'),
(8, 5, 5, 2, 'reject', 'Interesting', 'Promising results', '2027-02-08'),
(9, 6, 1, 3, 'reject', 'Good', 'WEak ', '2027-02-09'),
(10, 7, 5, 4, 'accept', 'Interesting', 'Not ready ', '2027-02-10'),
(11, 8, 7, 5, 'accept', 'Bad', 'REview', '2027-02-11');