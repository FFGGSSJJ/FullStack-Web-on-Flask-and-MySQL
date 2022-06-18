-- HW1.2
SELECT NetId, Score
FROM (
    SELECT Enrollments.CRN, MAX(Score) AS maxS, MIN(Score) AS minS
    FROM Enrollments JOIN Courses ON Enrollments.CRN = Courses.CRN
    WHERE Courses.Department = 'STAT'
    GROUP BY Enrollments.CRN) AS A NATURAL JOIN Enrollments
WHERE Score = maxS OR Score = minS
ORDER BY NetId ASC, Score DESC


-- HW1.3
SELECT Department, min(avgS) AS minAvgScore
FROM (
    SELECT Department, CRN, FLOOR(AVG(Score)) as avgS
    FROM Enrollments NATURAL JOIN Courses
    GROUP BY Department, CRN ) AS A 
GROUP BY Department
ORDER BY minAvgScore ASC, Department ASC


-- HW1.4
SELECT BrandName, CEO, YearEstablished, SUM(Price) AS totalAmount
FROM Brands NATURAL JOIN Products NATURAL JOIN Purchases
WHERE YearEstablished >= 2010
GROUP BY BrandName, CEO, YearEstablished
ORDER BY BrandName ASC, totalAmount DESC


-- HW1.5
SELECT maxScore, Department, Title
FROM (
    SELECT ROUND(MAX(Score),1) AS maxScore, CRN, Title, Department
    FROM Courses NATURAL JOIN Enrollments
    WHERE Department = 'Statistics' OR Department = 'Economics'
    GROUP BY CRN, Title, Department
    ) AS A
WHERE maxScore <= 80.0
ORDER BY maxScore ASC, Title ASC



-- HW1.6
(
SELECT Students.NetId, FirstName, LastName, Score
FROM (Students JOIN Enrollments ON Students.NetId = Enrollments.NetId JOIN Courses ON Courses.CRN = Enrollments.CRN) JOIN 
    (SELECT CRN, MIN(Score) AS minECE
    FROM Enrollments NATURAL JOIN Courses
    WHERE Courses.Department = 'ECE'
    GROUP BY CRN) AS A ON A.CRN = Enrollments.CRN
WHERE Students.Department = 'CS' AND Courses.Department = 'ECE' AND Score = minECE 
)
UNION
(
SELECT Students.NetId, FirstName, LastName, Score
FROM (Students JOIN Enrollments ON Students.NetId = Enrollments.NetId JOIN Courses ON Courses.CRN = Enrollments.CRN) JOIN 
    (SELECT CRN, MIN(Score) AS minCS
    FROM Enrollments NATURAL JOIN Courses
    WHERE Courses.Department = 'CS'
    GROUP BY CRN) AS A ON A.CRN = Enrollments.CRN
WHERE Students.Department = 'ECE' AND Courses.Department = 'CS' AND Score = minCS
)
ORDER BY Score



-- HW1.7
SELECT A.Title, A.Instructor
FROM
(
SELECT Title, Instructor, COUNT(Students.NetId) AS numCS
FROM Students JOIN Enrollments ON Students.NetId = Enrollments.NetId JOIN Courses ON Enrollments.CRN = Courses.CRN
WHERE Courses.Department = 'CS' AND Students.Department = 'CS'
GROUP BY Title, Instructor
) AS A 
JOIN
(
SELECT Title, Instructor, COUNT(Students.NetId) AS numNCS
FROM Students JOIN Enrollments ON Students.NetId = Enrollments.NetId JOIN Courses ON Enrollments.CRN = Courses.CRN
WHERE Courses.Department = 'CS' AND Students.Department <> 'CS'
GROUP BY Title, Instructor
) AS B 
ON (A.Title = B.Title AND A.Instructor = B.Instructor)
WHERE numCS < numNCS
ORDER BY Instructor, Title


-- HW1.8
SELECT FirstName, LastName, PhoneNumber
FROM Customers JOIN Purchases ON Customers.CustomerId = Purchases.CustomerId JOIN
    (SELECT ProductId, MAX(Price) AS maxPrice
    FROM Purchases NATURAL JOIN Products
    WHERE BrandName = 'Apple'
    GROUP BY ProductId
    ) AS A ON A.ProductId = Purchases.ProductId
WHERE Price = maxPrice
ORDER BY Customers.CustomerId DESC
