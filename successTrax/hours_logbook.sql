CREATE TABLE IF NOT EXISTS hours_logbook (
log_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
training_id INT NOT NULL,
training_date DATETIME NOT NULL,
hours REAL NOT NULL,
category VARCHAR(30) NOT NULL,
cleanup VARCHAR(3) NOT NULL,
changeover VARCHAR(3) NOT NULL
);