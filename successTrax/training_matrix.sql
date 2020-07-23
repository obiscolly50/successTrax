CREATE TABLE IF NOT EXISTS training_matrix (
matrix_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
training_id INTEGER NOT NULL UNIQUE,
safety_complete VARCHAR(3) NOT NULL CHECK (safety_complete IN ("Yes", "No")) DEFAULT "No",
sop_complete VARCHAR(3) NOT NULL CHECK (sop_complete IN ("Yes", "No")) DEFAULT "No",
qms_complete VARCHAR(3) NOT NULL CHECK (qms_complete IN ("Yes", "No")) DEFAULT "No",
area_fam_complete VARCHAR(3) NOT NULL CHECK (area_fam_complete IN ("Yes", "No")) DEFAULT "No",
le_complete VARCHAR(3) NOT NULL CHECK (le_complete IN ("Yes", "No")) DEFAULT "No",
test1_complete VARCHAR(3) NOT NULL CHECK (test1_complete IN ("Yes", "No")) DEFAULT "No",
test2_complete VARCHAR(3) NOT NULL CHECK (test2_complete IN ("Yes", "No")) DEFAULT "No",
test3_complete VARCHAR(3) NOT NULL CHECK (test3_complete IN ("Yes", "No")) DEFAULT "No",
cleanup_complete VARCHAR(3) NOT NULL CHECK (cleanup_complete IN ("Yes", "No")) DEFAULT "No",
changeover_complete VARCHAR(3) NOT NULL CHECK (changeover_complete IN ("Yes", "No")) DEFAULT "No",
signoff_complete VARCHAR(3) NOT NULL CHECK (signoff_complete IN ("Yes", "No")) DEFAULT "No",
FOREIGN KEY(training_id) REFERENCES training_status(training_id)
);

