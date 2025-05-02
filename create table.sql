CREATE TABLE IF NOT EXISTS AccountPassword (
    Account CHAR(10) PRIMARY KEY,
    Occupation TEXT('student', 'teacher', 'admin'),
    Password VARCHAR(255)
);