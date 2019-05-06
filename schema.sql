CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY,
    firstName TEXT,
    lastName TEXT
);

CREATE TABLE IF NOT EXISTS quiz(
    id INTEGER PRIMARY KEY,
    subject TEXT,
    questions INT,
    quizDate DATE
);

CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY,
    quizid INT,
    studentid INT,
    score INT
);

