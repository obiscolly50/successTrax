CREATE TABLE IF NOT EXISTS employees (
user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
employee_id INT UNIQUE NOT NULL,
first_name VARCHAR(50) NOT NULL,
mid_name VARCHAR(50),
last_name VARCHAR(50) NOT NULL,
primary_posting VARCHAR(60) NOT NULL DEFAULT "None",
shift VARCHAR(5) DEFAULT "None",
department VARCHAR(30),
job_type VARCHAR(10) NOT NULL CHECK (job_type IN ("Hourly", "Staff")),
phone VARCHAR(15),
email VARCHAR(15),
employment_date DATETIME,
employment_status VARCHAR(15) NOT NULL DEFAULT "Employed"
);