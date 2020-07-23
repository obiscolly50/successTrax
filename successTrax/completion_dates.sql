CREATE TABLE IF NOT EXISTS completion_dates (
completion_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
training_id INTEGER NOT NULL UNIQUE,
safety_completed DATETIME DEFAULT NULL,
sop_completed DATETIME DEFAULT NULL,
qms_completed DATETIME DEFAULT NULL,
area_fam_completed DATETIME DEFAULT NULL,
le_completed DATETIME DEFAULT NULL,
test1_completed DATETIME DEFAULT NULL,
test2_completed DATETIME DEFAULT NULL,
test3_completed DATETIME DEFAULT NULL,
cleanup_completed DATETIME DEFAULT NULL,
changeover_completed DATETIME DEFAULT NULL,
signoff_completed DATETIME DEFAULT NULL,
FOREIGN KEY(training_id) REFERENCES training_status(training_id)
);