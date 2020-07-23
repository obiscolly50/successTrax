CREATE TABLE IF NOT EXISTS training_status (
training_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
employee_id INTEGER,
training_position VARCHAR(60) NOT NULL,
category VARCHAR(30) NOT NULL,
start_date DATETIME NOT NULL,
end_date DATETIME,
training_shift VARCHAR(4),
area_fam_hrs REAL DEFAULT NULL,
le_hrs REAL DEFAULT NULL,
test1_score REAL DEFAULT NULL,
test2_score REAL DEFAULT NULL,
test3_score REAL DEFAULT NULL,
cleanup_hrs REAL DEFAULT NULL,
changeover_hrs REAL DEFAULT NULL,
FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
);

