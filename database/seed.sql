BEGIN;

INSERT INTO app_user
(user_id, given_name, surname, email, affiliation, country, phone_number)
VALUES
(1, 'Arman', 'Armanov', 'arman.armanov@example.com', 'NU', 'Kazakhstan', '+77010000001'),
(2, 'Amina', 'Aminova', 'amina.aminova@example.com', 'NU', 'Kazakhstan', '+77010000002'),
(3, 'Daniyar', 'Sadykov', 'daniyar@example.com', 'NU', 'Kazakhstan', '+77010000003'),
(4, 'Aliya', 'Bekova', 'aliya@example.com', 'KBTU', 'Kazakhstan', '+77010000004'),
(5, 'John', 'Smith', 'john@example.com', 'MIT', 'USA', '+12025550001'),
(6, 'Sara', 'Kim', 'sara@example.com', 'KAIST', 'South Korea', '+82025550001'),
(7, 'Michael', 'Brown', 'michael@example.com', 'Stanford', 'USA', '+12025550002'),
(8, 'Madina', 'Omarova', 'madina@example.com', 'NU', 'Kazakhstan', '+77010000008'),
(9, 'David', 'Lee', 'david@example.com', 'Oxford', 'UK', '+440755500001'),
(10, 'Emma', 'Wilson', 'emma@example.com', 'Harvard', 'USA', '+12025550003'),
(11, 'Timur', 'Nurgali', 'timur@example.com', 'NU', 'Kazakhstan', '+77010000011'),
(12, 'Laura', 'Garcia', 'laura@example.com', 'UCLA', 'USA', '+12025550004');

INSERT INTO author (author_id, orcid)
VALUES
(2, '0000-0002-0000-0002'),
(3, '0000-0003-0000-0003'),
(4, NULL),
(6, '0000-0006-0000-0006'),
(8, NULL),
(9, '0000-0009-0000-0009'),
(11, NULL),
(12, '0000-0012-0000-0012');

INSERT INTO author_research_area (author_id, area_label)
VALUES
(2, 'Machine Learning'),
(2, 'Data Science'),
(3, 'Artificial Intelligence'),
(4, 'Databases'),
(6, 'Robotics'),
(8, 'Computer Vision'),
(9, 'Machine Learning'),
(11, 'Data Science'),
(12, 'Software Engineering');

INSERT INTO reviewer (reviewer_id, years_experience)
VALUES
(1, 5),
(3, 4),
(5, 8),
(6, 2),
(7, 6),
(9, 3),
(10, 7);

INSERT INTO reviewer_expertise (reviewer_id, area_label)
VALUES
(1, 'Databases'),
(1, 'Machine Learning'),
(3, 'Artificial Intelligence'),
(5, 'Databases'),
(5, 'Data Science'),
(6, 'Robotics'),
(7, 'Databases'),
(9, 'Machine Learning'),
(10, 'Computer Vision');

INSERT INTO conference
(name, acronym, description, city, country,
 start_date, end_date, submission_deadline, review_deadline)
VALUES
('International Conference on Computer Science',
 'ICCS 2026',
 'Conference on computer science and technology',
 'Astana', 'Kazakhstan',
 '2026-12-10', '2026-12-12', '2026-10-01', '2026-11-15'),

('International AI Conference',
 'AI 2026',
 'Conference on artificial intelligence',
 'Almaty', 'Kazakhstan',
 '2026-12-15', '2026-12-17', '2026-10-10', '2026-11-20'),

('Global Computing Conference',
 'GCC 2026',
 'Conference on global computing research',
 'Tokyo', 'Japan',
 '2027-01-10', '2027-01-12', '2026-11-01', '2026-12-01');

INSERT INTO conference_host (conference_id, host_name)
VALUES
(1, 'Nazarbayev University'),
(1, 'Astana IT University'),
(2, 'Al-Farabi Kazakh National University'),
(3, 'University of Tokyo');

INSERT INTO conference_reviewer (conference_id, reviewer_id)
VALUES
(1, 1), (1, 5), (1, 7),
(2, 1), (2, 6), (2, 9),
(3, 10);

INSERT INTO track
(conference_id, name, description, research_area, coordinator_id)
VALUES
(1, 'Data Science', 'Research in data science', 'Data Science', 1),
(1, 'Cybersecurity', 'Research in cybersecurity', 'Security', 5),
(2, 'Artificial Intelligence', 'AI research track', 'Artificial Intelligence', 6),
(3, 'Computing Systems', 'Research in computing systems', 'Computer Science', 10);

INSERT INTO conference_session
(conference_id, title, session_date, start_time, end_time, room_label, chair_id)
VALUES
(1, 'Machine Learning Session', '2026-12-10',
 '09:00', '11:00', 'Room A', 7),

(1, 'Empty Research Session', '2026-12-10',
 '13:00', '15:00', 'Room B', 5),

(2, 'AI Research Session', '2026-12-15',
 '10:00', '12:00', 'Room C', 9);

INSERT INTO paper
(track_id, title, abstract, submission_date, status, session_id)
VALUES
(1, 'Machine Learning for Healthcare',
 'This paper studies machine learning methods for healthcare applications.',
 '2026-09-01', 'accepted', 1),

(1, 'Deep Learning Applications',
 'This research explores deep learning models and their applications.',
 '2026-09-02', 'accepted', NULL),

(1, 'Data Analysis in Modern Systems',
 'This paper discusses modern data analysis techniques.',
 '2026-09-03', 'accepted', NULL),

(1, 'Database Optimization',
 'This paper investigates database optimization methods.',
 '2026-09-04', 'submitted', NULL),

(1, 'Neural Networks for Prediction',
 'This study uses neural networks for prediction tasks.',
 '2026-09-05', 'under review', NULL),

(1, 'AI in Education',
 'This paper examines artificial intelligence in education.',
 '2026-09-06', 'under review', NULL),

(1, 'Computer Vision Methods',
 'This paper presents computer vision methods.',
 '2026-09-07', 'rejected', NULL),

(3, 'Robotics and Automation',
 'This paper explores robotics and automation systems.',
 '2026-09-08', 'rejected', NULL),

(3, 'Machine Learning in Research',
 'This paper explores machine learning in scientific research.',
 '2026-09-09', 'withdrawn', NULL),

(3, 'Data Science Applications',
 'This paper discusses data science applications.',
 '2026-09-10', 'withdrawn', NULL);

INSERT INTO paper_keyword (paper_id, keyword)
VALUES
(1, 'Machine Learning'), (1, 'Healthcare'),
(2, 'Deep Learning'), (2, 'AI'),
(3, 'Data Analysis'),
(4, 'Databases'),
(5, 'Neural Networks'),
(6, 'Education'),
(7, 'Computer Vision'),
(8, 'Robotics'),
(9, 'Machine Learning'),
(10, 'Data Science');

INSERT INTO paper_author
(paper_id, author_id, author_position, is_corresponding)
VALUES
(1, 2, 1, TRUE),
(1, 4, 2, FALSE),

(2, 3, 1, TRUE),
(2, 8, 2, FALSE),

(3, 4, 1, TRUE),
(3, 11, 2, FALSE),

(4, 8, 1, TRUE),

(5, 2, 1, TRUE),
(5, 6, 2, FALSE),

(6, 11, 1, TRUE),
(6, 12, 2, FALSE),

(7, 3, 1, TRUE),

(8, 4, 1, TRUE),
(8, 8, 2, FALSE),

(9, 2, 1, TRUE),
(9, 11, 2, FALSE),

(10, 2, 1, TRUE),
(10, 12, 2, FALSE);

INSERT INTO paper_version
(paper_id, version_no, file_location, uploaded_at, change_note)
VALUES
(1, 1, 'papers/paper1_v1.pdf', '2026-09-01 10:00:00', 'Initial submission'),
(1, 2, 'papers/paper1_v2.pdf', '2026-09-05 12:00:00', 'Updated experiments'),
(2, 1, 'papers/paper2_v1.pdf', '2026-09-02 11:00:00', 'Initial submission'),
(3, 1, 'papers/paper3_v1.pdf', '2026-09-03 09:00:00', 'Initial submission'),
(4, 1, 'papers/paper4_v1.pdf', '2026-09-04 14:00:00', 'Initial submission'),
(5, 1, 'papers/paper5_v1.pdf', '2026-09-05 15:00:00', 'Initial submission'),
(6, 1, 'papers/paper6_v1.pdf', '2026-09-06 16:00:00', 'Initial submission'),
(7, 1, 'papers/paper7_v1.pdf', '2026-09-07 10:00:00', 'Initial submission'),
(8, 1, 'papers/paper8_v1.pdf', '2026-09-08 11:00:00', 'Initial submission'),
(9, 1, 'papers/paper9_v1.pdf', '2026-09-09 12:00:00', 'Initial submission'),
(10, 1, 'papers/paper10_v1.pdf', '2026-09-10 13:00:00', 'Initial submission');

INSERT INTO review
(paper_id, reviewer_id, overall_score, recommendation,
 comments_for_authors, confidential_comments, review_submission_date)
VALUES
(1, 5, 5, 'accept', 'Excellent paper.', 'Strong contribution.', '2026-10-01'),
(1, 7, 4, 'accept', 'Good methodology.', 'Minor issues.', '2026-10-02'),

(2, 1, 4, 'accept', 'Interesting research.', 'Good quality.', '2026-10-03'),
(2, 5, 5, 'accept', 'Very clear paper.', 'Recommend acceptance.', '2026-10-04'),

(3, 1, 4, 'accept', 'Well-written paper.', 'No major issues.', '2026-10-05'),
(3, 7, 3, 'reject', 'Needs improvement.', 'Some weaknesses.', '2026-10-06'),

(4, 1, 3, 'reject', 'More experiments needed.', 'Insufficient evaluation.', '2026-10-07'),

(5, 5, 4, 'accept', 'Good approach.', 'Promising results.', '2026-10-08'),

(6, 1, 3, 'reject', 'The paper needs more detail.', 'Weak evaluation.', '2026-10-09'),

(7, 5, 2, 'reject', 'The contribution is unclear.', 'Not ready for publication.', '2026-10-10'),

(9, 5, 3, 'reject', 'The paper was withdrawn.', 'Review record for testing.', '2026-10-11'),

(10, 1, 2, 'reject', 'The paper was withdrawn.', 'Review record for testing.', '2026-10-12');

SELECT setval(
    pg_get_serial_sequence('app_user', 'user_id'),
    (SELECT MAX(user_id) FROM app_user)
);

COMMIT;
