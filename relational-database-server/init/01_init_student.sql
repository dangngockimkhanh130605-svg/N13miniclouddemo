CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    dob DATE,
    major VARCHAR(50)
);

INSERT INTO students (student_id, fullname, dob, major) VALUES 
('52300208', 'Dang Ngoc Kim Khanh', '2005-01-01', 'Software Engineering'),
('52300206', 'Vu Khanh Huyen', '2005-02-02', 'Networking'),
('52300223', 'Le Diem My', '2005-03-03', 'Data Science');
