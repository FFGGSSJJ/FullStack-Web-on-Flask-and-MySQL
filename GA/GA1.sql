-- GA1.3
-- For students in the 'CS' department, write one SQL query to return their first and last name, and the CRN, title, score and credits of courses they have enrolled in. Sort the result in an ascending order by Score and in a decending order by student LastName.
-- Do NOT output duplicate rows and use Natural Join when possible.
SELECT *
FROM Students JOIN Enrollments ON Students.NetId = Enrollments.NetId JOIN Courses ON Enrollments.CRN = Courses.CRN
WHERE Students.Department = 'CS'
ORDER BY Score ,LastName DESC;