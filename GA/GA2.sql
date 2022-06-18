-- GA2.1
-- Write one SQL query that returns the Title, Department 
-- and Instructor of courses taken by students whose NetId contains swift 
-- and who received a score higher than 90. Order the results 
-- in descending order of Title and ascending order of Instructor.
SELECT Title, Department, Instructor
FROM Courses
WHERE CRN IN (SELECT CRN FROM Enrollments WHERE NetId LIKE '%swift%' AND Score > 90)
ORDER BY Title DESC, Instructor ASC




-- GA2.2
-- Write one SQL query that returns the NetID, first and last name, 
-- and Department of students who have achieved a score higher than 80 in a course offered in ‘CS’ department. 
-- Return the result in a decending order by the student NetId.
SELECT *
FROM Students s
WHERE EXISTS(
	SELECT *
	FROM Enrollments NATURAL JOIN Courses 
-- 	FROM Enrollments JOIN Courses ON Enrollments.CRN = Courses.CRN
	WHERE s.NetId = Enrollments.NetId AND Courses.Department = 'CS' AND Enrollments.Score >= 80
)
ORDER BY s.NetId DESC