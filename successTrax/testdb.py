from cs50 import SQL

db = SQL("sqlite:///training.db")

rows = db.execute("SELECT * FROM jobs")

jobs = {}

for row in rows:
    if row['department'] in jobs:
         jobs[row['department']].append(row['job'])
    else:
        jobs[row['department']] = [row['job']]

print(jobs)