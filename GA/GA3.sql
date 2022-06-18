-- GA3.1
-- Write one SQL query to find the average salary of employees with the same job title. List the jobTitle and the average salary. 
-- Order the result in ascending order by the average salary and in descending order by jobTitle.
SELECT jobTitle, AVG(salary) AS AvgSalary
FROM Employee
GROUP BY jobTitle
ORDER BY AvgSalary ASC, jobTitle DESC


-- GA3.2
-- Write one SQL query to find the number of employees for each department. 
-- List the department name, location, and the number of employees (don't forget to include departments with no employees). 
-- Return the result in ascending order by employees count and in a descending order by the department name.
SELECT deptName, deptLocation, COUNT(empID) AS NumEmp
FROM Department LEFT OUTER JOIN Employee ON Department.deptID = Employee.deptID
GROUP BY deptName, deptLocation
ORDER BY NumEmp ASC, deptName DESC