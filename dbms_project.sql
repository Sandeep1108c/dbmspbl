-- Create and use the database
CREATE DATABASE IF NOT EXISTS dbms_project;
USE dbms_project;

-- Drop table if exists to start fresh
DROP TABLE IF EXISTS Students;

-- Create table
CREATE TABLE Students (
    Student_ID INT PRIMARY KEY,
    NAME VARCHAR(50),
    Department VARCHAR(30),
    Age INT,
    Marks INT
);

-- Insert data
INSERT INTO Students VALUES
(1, 'Rahul', 'CSE', 20, 85),
(2, 'Priya', 'ECE', 21, 78),
(3, 'Arjun', 'ME', 18, 92),
(4, 'Sneha', 'EEE', 22, 68),
(5, 'Kiran', 'ECE', 20, 88);

-- Query 1: Select distinct departments
SELECT DISTINCT Department FROM Students;

-- Query 2: CSE students with marks > 80
SELECT * FROM Students WHERE Department = 'CSE' AND Marks > 80;

-- Query 3: CSE or ECE students
SELECT * FROM Students WHERE Department = 'CSE' OR Department = 'ECE';

-- Query 4: Students NOT in CSE
SELECT * FROM Students WHERE NOT Department = 'CSE';

-- Query 5: Students with marks between 70 and 90
SELECT * FROM Students WHERE Marks BETWEEN 70 AND 90;

-- Query 6: Order by marks ascending
SELECT * FROM Students ORDER BY Marks ASC;

-- Query 7: Order by marks descending
SELECT * FROM Students ORDER BY Marks DESC;

-- Query 8: Students where Department is NULL
SELECT * FROM Students WHERE Department IS NULL;

-- Query 9: Top 3 students by marks descending
SELECT * FROM Students ORDER BY Marks DESC LIMIT 3;

-- Query 10: Minimum marks
SELECT MIN(Marks) AS Minimum_Marks FROM Students;

-- Query 11: Maximum marks
SELECT MAX(Marks) AS Maximum_Marks FROM Students;

-- Query 12: Average marks
SELECT AVG(Marks) AS Average_Marks FROM Students;

-- Query 13: Sum of marks
SELECT SUM(Marks) AS Total_Marks FROM Students;

-- Query 14: Count of students
SELECT COUNT(*) AS Total_Students FROM Students;
