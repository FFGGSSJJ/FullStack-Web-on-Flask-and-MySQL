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

--HW 1.9
CREATE TRIGGER BoGo
    BEFORE INSERT ON Purchases
    FOR EACH ROW
    BEGIN
        SET @PurNum = (SELECT COUNT(CustomerId) FROM Purchases
                       WHERE ProductId = new.ProductId AND CustomerId = new.CustomerId
                       GROUP BY CustomerId);
        IF MOD(@PurNum,2) = 1 THEN
            SET new.Price = new.Price * 0.7;
        END IF;
    END;

INSERT INTO Purchases
SELECT PurchaseId + 1000, CustomerId, ProductId, Price FROM Purchases;
INSERT INTO Purchases
SELECT PurchaseId + 2000, CustomerId, ProductId, Price FROM Purchases;
INSERT INTO Purchases
SELECT PurchaseId + 4000, CustomerId, ProductId, Price FROM Purchases;

SELECT * FROM Purchases
ORDER BY PurchaseId DESC 
LIMIT 10



create procedure Result()
begin
declare done int default 0;
declare curr int;
declare avg_score int;
declare letter VARCHAR(1);
declare tit VARCHAR(255);
declare course_cur cursor for select distinct CRN from Courses;
declare continue handler for not found set done = 1;

drop table if exists FinalTable;
create table FinalTable(CRN INT, Title VARCHAR(255), AverageScore INT, Rating VARCHAR(1));

open course_cur;
repeat
    fetch course_cur into curr;
    set avg_score = (select avg(Score) from Enrollments where curr = CRN);
    set tit = (select distinct Title from Courses where curr = CRN);
    if (avg_score>=90) then set letter = 'A' ;
    elseif (avg_score>=80) then set letter = 'B';
    elseif (avg_score>=70) then set letter = 'C' ;
    elseif (avg_score>=60) then set letter = 'D' ;
    else  set letter = 'E';
    end if;
    insert into FinalTable values(curr, tit, avg_score, letter);
until done
end repeat;

close course_cur;

select distinct Title, Rating from FinalTable order by Rating, Title limit 5;
end

-- HW1.10
CREATE PROCEDURE Result()
BEGIN
    DECLARE flag INT DEFAULT 0;
    DECLARE CurrCRN INT;
    DECLARE Ctitle VARCHAR(255);
    DECLARE Letter VARCHAR(1);
    DECLARE avgS REAL;
    DECLARE CourCur CURSOR FOR SELECT DISTINCT CRN FROM Courses;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET flag = 1;

    DROP TABLE IF EXISTS FinalTable;
    CREATE TABLE FinalTable (
        CRN INT, 
        Title VARCHAR(255),
        AverageScore REAL, 
        Rating VARCHAR(1) DEFAULT 'A'
    );
    
    OPEN CourCur;
    
    REPEAT
        FETCH CourCur INTO CurrCRN;
        SET avgS = (SELECT AVG(Score) FROM Enrollments WHERE CurrCRN = CRN);
        SET Ctitle = (SELECT DISTINCT Title FROM Courses WHERE CurrCRN = CRN);
        
        IF avgS >= 90 THEN SET Letter = 'A';
        ELSEIF avgS >= 80 THEN SET Letter = 'B';
        ELSEIF avgS >= 70 THEN SET Letter = 'C';
        ELSEIF avgS >= 60 THEN SET Letter = 'D';
        ELSE SET Letter = 'E';
        END IF;
        
        INSERT INTO FinalTable
        VALUES(CurrCRN, Ctitle, avgS, Letter);
    UNTIL flag
    END REPEAT;
    
    CLOSE CourCur;
    
    SELECT DISTINCT Title, Rating FROM FinalTable 
    ORDER BY Rating, Title
    LIMIT 5;
END;