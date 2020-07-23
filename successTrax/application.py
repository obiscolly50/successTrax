import os
from cs50 import SQL
from tempfile import mkdtemp
from flask_session import Session
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from login import login_required

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(16)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///training.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

@app.route("/add_employee", methods=["GET","POST"])
@login_required
def add_employee():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM jobs")
        jobs = {}
        for row in rows:
            if row['department'] in jobs:
                 jobs[row['department']].append(row['job'])
            else:
                jobs[row['department']] = [row['job']]
        return render_template("add_employee.html", jobs=jobs)

    else: #IF POST
        first = request.form.get('firstName')
        mid = request.form.get('midName')
        last = request.form.get('lastName')
        empID = request.form.get('employeeID')
        jobType = request.form.get('jobType')
        shift = request.form.get('shift')
        dept = request.form.get('dept')
        primaryJob = request.form.get('primaryJob')
        phone = request.form.get('phone')
        email = request.form.get('email')
        dateEmployed = request.form.get('dateEmployed')
        status = request.form.get('empStatus')

        #check if any of the required fields are empty
        if not (first and last and empID and jobType and shift and dept and primaryJob and phone and dateEmployed and status):
            flash("You must fill out the form before submitting", "danger")
            return redirect("/add_employee")

        #check if employee already exists
        employeeExists = db.execute("SELECT * FROM employees WHERE employee_id=:empID", empID=empID)
        if employeeExists:
            flash("An employee with that employeeID already exists in record. Please ensure the employee ID is correct.","danger")
            return redirect("/add_employee")
        #add employee to database
        db.execute("INSERT INTO employees (first_name, mid_name, last_name, employee_id, job_type, shift, department,\
                    primary_posting, phone, email, employment_date, employment_status) \
                    VALUES (:first, :mid, :last, :empID, :jobType, :shift, :dept, :primaryJob, :phone, :email, :dateEmployed, :status)", \
                    first=first, mid=mid, last=last, empID=empID, jobType=jobType, shift=shift, dept=dept, primaryJob=primaryJob, phone=phone, email=email,\
                    dateEmployed=dateEmployed, status=status)

        flash("Employee has been added to record!","success")
        return redirect("/add_employee")

@app.route("/create_training_plan", methods=["GET", "POST"])
@login_required
def create_training_plan():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM jobs")
        jobs = {}
        for row in rows:
            if row['department'] in jobs:
                 jobs[row['department']].append(row['job'])
            else:
                jobs[row['department']] = [row['job']]
        return render_template("create_training_plan.html", jobs=jobs)
    else: #POST method
        dept = request.form.get('dept')
        job = request.form.get('primaryJob')
        safety_req = "Yes" if request.form.get('safety') else "No"
        sop_req = "Yes" if request.form.get('sop-review') else "No"
        qms_req = "Yes" if request.form.get('qms-review') else "No"
        area_fam_req = "Yes" if request.form.get('area-fam') else "No"
        area_fam_hrs = None if not request.form.get('area-fam-hrs') else request.form.get('area-fam-hrs')
        le_req = "Yes" if request.form.get('line-exp') else "No"
        le_hrs = None if not request.form.get('line-exp-hrs') else request.form.get('line-exp-hrs')
        test_req = "Yes" if request.form.get('test') else "No"
        num_test = None if not request.form.get('test-num') else request.form.get('test-num')
        test1_trigger = request.form.get('test1-hrs', None)
        test1_pass = request.form.get('test1-pass', None)
        test2_trigger = request.form.get('test2-hrs', None)
        test2_pass =  request.form.get('test2-pass', None)
        test3_trigger = request.form.get('test3-hrs', None)
        test3_pass =  request.form.get('test3-pass', None)
        cleanup_req = "Yes" if request.form.get('cleanup-exp') else "No"
        cleanup_hrs = None if not request.form.get('cleanup-hrs') else request.form.get('cleanup-hrs')
        changeover_req = "Yes" if request.form.get('changeover-exp') else "No"
        changeover_hrs = None if not request.form.get('changeover-hrs') else request.form.get('changeover-hrs')
        signoff = "Yes" if request.form.get('signoff') else "No"

        #check if training plan already exists
        planExists = db.execute("SELECT * FROM training_plan WHERE job=:job", job=job)
        if planExists:
            flash(f"A training plan already exists for the {job} position","danger")
            return redirect("/create_training_plan")

        #add training plan to DB
        db.execute("INSERT INTO training_plan (department, job, safety_req, sop_req, qms_req, area_fam_req, area_fam_hrs, le_req,\
                    le_hrs, test_req, num_test, test1_trigger, test1_pass, test2_trigger, test2_pass, test3_trigger, test3_pass,\
                    cleanup_req, cleanup_hrs, changeover_req, changeover_hrs, signoff_req) \
                    VALUES (:dept, :job, :safety_req, :sop_req, :qms_req, :area_fam_req, :area_fam_hrs, :le_req,\
                    :le_hrs, :test_req, :num_test, :test1_trigger, :test1_pass, :test2_trigger, :test2_pass, :test3_trigger, :test3_pass, \
                    :cleanup_req, :cleanup_hrs, :changeover_req, :changeover_hrs, :signoff)", \
                    dept=dept, job=job, safety_req=safety_req, sop_req=sop_req, qms_req=qms_req, area_fam_req=area_fam_req, area_fam_hrs=area_fam_hrs, le_req=le_req,\
                    le_hrs=le_hrs, test_req=test_req, num_test=num_test, test1_trigger=test1_trigger, test1_pass=test1_pass, test2_trigger=test2_trigger, \
                    test2_pass=test2_pass, test3_trigger=test3_trigger, test3_pass=test3_pass, cleanup_req=cleanup_req, cleanup_hrs=cleanup_hrs, \
                    changeover_req=changeover_req, changeover_hrs=changeover_hrs, signoff=signoff)

        flash(f"Training plan has been successfully created for the {job} position!","success")
        return redirect("/create_training_plan")


@app.route("/create_new_training", methods=["GET", "POST"])
@login_required
def create_new_training():
    if request.method == "GET":
        rows = db.execute("SELECT department, job FROM training_plan")
        jobs = {}
        for row in rows:
            if row['department'] in jobs:
                 jobs[row['department']].append(row['job'])
            else:
                jobs[row['department']] = [row['job']]
        return render_template("create_new_training.html", jobs=jobs)
    else: #for POST
        #retrieve values from form
        empID = request.form.get('employeeID')
        dept = request.form.get('dept')
        position = request.form.get('primaryJob')
        category = request.form.get('category')
        date = request.form.get('start-date')
        shift = request.form.get('shift')

        #check if form is filled correctly
        if not (empID and dept and position and category and date):
            flash("You must input all required field", "danger")
            return redirect("/create_new_training")

        #check if employee exists
        employeeExists = db.execute("SELECT * FROM employees WHERE employee_id=:empID", empID=empID)
        if not employeeExists:
            flash("No employee with that Employee ID exists in record", "danger")
            return redirect("/create_new_training")

        #check if employee already training in position
        employee_training_exists = db.execute("SELECT * from training_status WHERE employee_id=:empID \
                                    AND training_position=:position", empID=empID, position=position)
        if employee_training_exists:
            flash("Employee is already trained or is training in this position", "danger")
            return redirect("/create_new_training")

        training_id = db.execute("INSERT INTO training_status(employee_id, training_position, category, start_date, end_date, training_shift)\
                    VALUES(:empID, :position, :category, :date, :end_date, :shift)", empID=empID, position=position, category=category, date=date, end_date=None, shift=shift)
        flash(f"New employee training record has been opened for {employeeExists[0]['first_name']} {employeeExists[0]['last_name']}", "success")

        db.execute("INSERT INTO training_matrix(training_id) VALUES(:training_id)", training_id=training_id)
        db.execute("INSERT INTO completion_dates(training_id) VALUES(:training_id)", training_id=training_id)
        return redirect("/create_new_training")


@app.route("/record_training_hours", methods=["GET", "POST"])
@login_required
def record_training_hours():
    if request.method == "GET":
        rows = db.execute("SELECT department, job FROM training_plan")
        jobs = {}
        for row in rows:
            if row['department'] in jobs:
                 jobs[row['department']].append(row['job'])
            else:
                jobs[row['department']] = [row['job']]
        return render_template("record_training_hours.html", jobs=jobs)
    else: #POST
        empID = request.form.get('employeeID')
        dept = request.form.get('dept')
        position = request.form.get('primaryJob')

       #check if user exists
        employeeExists = db.execute("SELECT * FROM employees WHERE employee_id=:empID", empID=empID)
        if not employeeExists:
            flash("No employee with that Employee ID exists in record", "danger")
            return redirect("/record_training_hours")

        #check if user is currently training in position
        employee_is_training = db.execute("SELECT * FROM training_status WHERE employee_id=:empID AND \
                                training_position=:position AND end_date IS NULL", empID=empID, position=position)

        if not employee_is_training:
            flash(f"Cannot complete operation. Either {employeeExists[0]['first_name']} {employeeExists[0]['last_name']} \
                has not begun training for the {position} position or has completed training", "danger")
            return redirect("/record_training_hours")

        training_id = employee_is_training[0]['training_id']

        #insert data into hours logbook
        for date, hours, category, cleanup, changeover in zip(request.form.getlist('date'),
                                                             request.form.getlist('hours'),
                                                             request.form.getlist('category'),
                                                             request.form.getlist('cleanup'),
                                                             request.form.getlist('changeover')):
            print("training_id:", training_id)
            db.execute("INSERT INTO hours_logbook(training_id, training_date, hours, category, cleanup, changeover) \
                        VALUES (:training_id, :date, :hours, :category, :cleanup, :changeover)", \
                        training_id=training_id, date=date, hours=hours, category=category, cleanup=cleanup, changeover=changeover)

        #update hours to global training status tracker
        #update Area fam hours
        area_fam_hrs = db.execute("SELECT SUM(hours) FROM hours_logbook WHERE training_id=:training_id AND category=:category", \
                        training_id=training_id, category="Area Familiarization")
        db.execute("UPDATE training_status SET area_fam_hrs=:area_fam_hrs WHERE training_id=:training_id", \
                    area_fam_hrs=area_fam_hrs[0]['SUM(hours)'], training_id=training_id)

        #update line experience hours
        le_hrs = db.execute("SELECT SUM(hours) FROM hours_logbook WHERE training_id=:training_id AND category=:category", \
                        training_id=training_id, category="Line Experience")
        db.execute("UPDATE training_status SET le_hrs=:le_hrs WHERE training_id=:training_id", \
                    le_hrs=le_hrs[0]['SUM(hours)'], training_id=training_id)

        #update cleanup experience hours
        cleanup_hrs = db.execute("SELECT SUM(hours) FROM hours_logbook WHERE training_id=:training_id AND cleanup=:cleanup", \
                        training_id=training_id, cleanup="Yes")
        db.execute("UPDATE training_status SET cleanup_hrs=:cleanup_hrs WHERE training_id=:training_id", \
                    cleanup_hrs=cleanup_hrs[0]['SUM(hours)'], training_id=training_id)

        #update changeover experience hours
        changeover_hrs = db.execute("SELECT SUM(hours) FROM hours_logbook WHERE training_id=:training_id AND changeover=:changeover", \
                        training_id=training_id, changeover="Yes")
        db.execute("UPDATE training_status SET changeover_hrs=:changeover_hrs WHERE training_id=:training_id", \
                    changeover_hrs=changeover_hrs[0]['SUM(hours)'], training_id=training_id)

        #update training matrix if hour requirements are met
        requirements = db.execute("SELECT * FROM training_plan WHERE job=:position", position=position)

        if area_fam_hrs[0]['SUM(hours)'] is not None:
            if area_fam_hrs[0]['SUM(hours)'] >= requirements[0]['area_fam_hrs']:
                db.execute("UPDATE training_matrix SET area_fam_complete:area_fam_complete WHERE training_id=:training_id", \
                        area_fam_complete="Yes", training_id=training_id)

        if le_hrs[0]['SUM(hours)'] is not None:
            if le_hrs[0]['SUM(hours)'] >= requirements[0]['le_hrs']:
                db.execute("UPDATE training_matrix SET le_complete=:le_complete WHERE training_id=:training_id", \
                        le_complete="Yes", training_id=training_id)

        if cleanup_hrs[0]['SUM(hours)'] is not None:
            if cleanup_hrs[0]['SUM(hours)'] >= requirements[0]['cleanup_hrs']:
                db.execute("UPDATE training_matrix SET cleanup_complete=:cleanup_complete WHERE training_id=:training_id", \
                        cleanup_complete="Yes", training_id=training_id)


        if changeover_hrs[0]['SUM(hours)'] is not None:
            if changeover_hrs[0]['SUM(hours)'] >= requirements[0]['changeover_hrs']:
                db.execute("UPDATE training_matrix SET changeover_complete=:changeover_complete WHERE training_id=:training_id", \
                        changeover_complete="Yes", training_id=training_id)

        flash("Training hours recorded succesfully!", "success")
        return redirect("/record_training_hours")

@app.route("/record_doc_review", methods=["GET", "POST"])
@login_required
def record_doc_review():
    if request.method == "GET":
        rows = db.execute("SELECT department, job FROM training_plan")
        jobs = {}
        for row in rows:
            if row['department'] in jobs:
                 jobs[row['department']].append(row['job'])
            else:
                jobs[row['department']] = [row['job']]
        return render_template("record_doc_review.html", jobs=jobs)

    else: #POST
        empID = request.form.get('employeeID')
        dept = request.form.get('dept')
        position = request.form.get('primaryJob')
        date = request.form.get('date')
        document = request.form.get('document')

        #check if employee exists
        employeeExists = db.execute("SELECT * FROM employees WHERE employee_id=:empID", empID=empID)
        if not employeeExists:
            flash("No employee with that Employee ID exists in record", "danger")
            return redirect("/record_doc_review")

        #check if employee is training in position
        employee_is_training = db.execute("SELECT * FROM training_status WHERE employee_id=:empID AND \
                                training_position=:position AND end_date IS NULL", empID=empID, position=position)

        if not employee_is_training:
            flash(f"Cannot complete operation. Either {employeeExists[0]['first_name']} {employeeExists[0]['last_name']} \
                has not begun training for the {position} position or has completed training", "danger")
            return redirect("/record_doc_review")

        training_id = employee_is_training[0]['training_id']


        requirements = db.execute("SELECT * FROM training_plan WHERE job=:position", position=position)
        completion = db.execute("SELECT * FROM training_matrix WHERE training_id=:training_id", training_id=training_id)

        if document == "SOP":
            #check if required to complete based on training plan
            if requirements[0]['sop_req'] == "No":
                flash(f"Cannot complete operation. According to the training plan, an SOP review is not required for the {position} position", "danger")
                return redirect("/record_doc_review")

            #check if document is completed already
            if completion[0]['sop_complete'] == "Yes":
                flash(f"Cannot complete operation. Employee has completed SOP review already", "danger")
                return redirect("/record_doc_review")

            #update training matrix and completion date tables
            db.execute("UPDATE training_matrix SET sop_complete=:sop_complete WHERE training_id=:training_id", sop_complete="Yes", training_id=training_id)
            db.execute("UPDATE completion_dates SET sop_completed=:date WHERE training_id=:training_id", date=date, training_id=training_id)
            flash(f"SOP review completion has been registered for employee", "success")
            return redirect("/record_doc_review")

        if document == "QMS":
            #check if required to complete based on training plan
            if requirements[0]['qms_req'] == "No":
                flash(f"Cannot complete operation. According to the training plan, a QMS review is not required for the {position} position", "danger")
                return redirect("/record_doc_review")

            #check if document is completed already
            if completion[0]['qms_complete'] == "Yes":
                flash(f"Cannot complete operation. Employee has completed QMS review already", "danger")
                return redirect("/record_doc_review")

        if document == "Safety":
            #check if required to complete based on training plan
            if requirements[0]['safety_req'] == "No":
                flash(f"Cannot complete operation. According to the training plan, a Safety review is not required for the {position} position", "danger")
                return redirect("/record_doc_review")

            #check if document is completed already
            if completion[0]['safety_complete'] == "Yes":
                flash(f"Cannot complete operation. Employee has completed safety review already", "danger")
                return redirect("/record_doc_review")

            #update training matrix and completion date tables
            db.execute("UPDATE training_matrix SET safety_complete=:safety_complete WHERE training_id=:training_id" , safety_complete="Yes", training_id=training_id)
            db.execute("UPDATE completion_dates SET safety_completed=:date WHERE training_id=:training_id", date=date, training_id=training_id)
            flash(f"Safety review completion has been registered for employee", "success")
            return redirect("/record_doc_review")

@app.route("/training_status", methods=["GET", "POST"])
@login_required
def training_status():
    if request.method == "GET":
        rows = db.execute("SELECT department, job FROM training_plan")
        jobs = {}
        for row in rows:
            if row['department'] in jobs:
                 jobs[row['department']].append(row['job'])
            else:
                jobs[row['department']] = [row['job']]
        return render_template("training_status.html", jobs=jobs)
    else: #POST
        empID = request.form.get('employeeID')
        dept = request.form.get('dept')
        position = request.form.get('primaryJob')

        #check if employee exists
        employeeExists = db.execute("SELECT * FROM employees WHERE employee_id=:empID", empID=empID)
        if not employeeExists:
            flash("No employee with that Employee ID exists in record", "danger")
            return redirect("/training_status")

        #check if employee is training in position
        employee_is_training = db.execute("SELECT * FROM training_status WHERE employee_id=:empID AND \
                                training_position=:position AND end_date IS NULL", empID=empID, position=position)
        if not employee_is_training:
            flash(f"Cannot complete operation. Either {employeeExists[0]['first_name']} {employeeExists[0]['last_name']} \
                has not begun training for the {position} position or has completed training", "danger")
            return redirect("/training_status")

        training_id = employee_is_training[0]['training_id']

        #select training status join training matrix join completion dates and requirements pass to next page
        status = db.execute("SELECT * FROM training_status  \
                            JOIN training_matrix ON training_status.training_id = training_matrix.training_id \
                            JOIN completion_dates ON training_matrix.training_id = completion_dates.training_id \
                            WHERE training_status.training_id=:training_id", training_id=training_id)

        requirements = db.execute("SELECT * FROM training_plan WHERE job=:position", position=position)
        #store items to report on
        checks = {}

        if requirements[0]['safety_req'] == "Yes":
            checks['Safety orientation'] = {}
            checks['Safety orientation']['target'] = requirements[0]['safety_req']
            checks['Safety orientation']['current'] = status[0]['safety_complete']
            checks['Safety orientation']['met'] = status[0]['safety_complete']

        if requirements[0]['sop_req'] == "Yes":
            checks['SOP review'] = {}
            checks['SOP review']['target'] = requirements[0]['sop_req']
            checks['SOP review']['current'] = status[0]['sop_complete']
            checks['SOP review']['met'] = status[0]['sop_complete']

        if requirements[0]['qms_req'] == "Yes":
            checks['QMS review'] = {}
            checks['QMS review']['target'] = requirements[0]['qms_req']
            checks['QMS review']['current'] = status[0]['qms_complete']
            checks['QMS review']['met'] = status[0]['qms_complete']

        if requirements[0]['area_fam_req'] == "Yes":
            checks['Area familiarization (hours)'] = {}
            checks['Area familiarization (hours)']['target'] = requirements[0]['area_fam_hrs']
            checks['Area familiarization (hours)']['current'] = status[0]['area_fam_hrs']
            checks['Area familiarization (hours)']['met'] = status[0]['area_fam_complete']

        if requirements[0]['le_req'] == "Yes":
            checks['Line experience (hours)'] = {}
            checks['Line experience (hours)']['target'] = requirements[0]['le_hrs']
            checks['Line experience (hours)']['current'] = status[0]['le_hrs']
            checks['Line experience (hours)']['met'] = status[0]['le_complete']

        if requirements[0]['test_req'] == "Yes":
            for x in range(requirements[0]['num_test']):
                checks[f'Test {x + 1} score (%)'] = {}
                checks[f'Test {x + 1} score (%)']['target'] = requirements[0][f'test{x + 1}_pass']
                checks[f'Test {x + 1} score (%)']['current'] = status[0][f'test{x + 1}_score']
                checks[f'Test {x + 1} score (%)']['met'] = status[0][f'test{x + 1}_complete']

        if requirements[0]['changeover_req'] == "Yes":
            checks['Changeover experience (hours)'] = {}
            checks['Changeover experience (hours)']['target'] = requirements[0]['changeover_hrs']
            checks['Changeover experience (hours)']['current'] = status[0]['changeover_hrs']
            checks['Changeover experience (hours)']['met'] = status[0]['changeover_complete']

        if requirements[0]['cleanup_req'] == "Yes":
            checks['Cleanup experience (hours)'] = {}
            checks['Cleanup experience (hours)']['target'] = requirements[0]['cleanup_hrs']
            checks['Cleanup experience (hours)']['current'] = status[0]['cleanup_hrs']
            checks['Cleanup experience (hours)']['met'] = status[0]['cleanup_complete']

        if requirements[0]['signoff_req'] == "Yes":
            checks['Supervisor signoff'] = {}
            checks['Supervisor signoff']['target'] = requirements[0]['signoff_req']
            checks['Supervisor signoff']['current'] = status[0]['signoff_complete']
            checks['Supervisor signoff']['met'] = status[0]['signoff_complete']


        print(checks)
        print(status)

        return render_template("checked_training_status.html", checks=checks, status=status, employee=employeeExists)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username", "danger")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password", "danger")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM login WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or request.form.get("password") != rows[0]['hash']:
            flash("Invalid username and/or password", "danger")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

"""
@app.route("/remove_employee")
def remove_employee():
    return render_template("remove_employee.html")

@app.route("/update_employee")
def update_employee():
    return render_template("update_employee.html")

@app.route("/lookup_employee")
def lookup_employee():
    return render_template("lookup_employee.html")

@app.route("/list_employees")
def list_employees():
    return render_template("list_employees.html")
"""