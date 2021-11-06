#I used the timedelta from the datetime
#when a user enter the activities without being registered when he want to see the result it will take him to the log in
# and then he can choose register and when he registered, 
# he will back to the main page and when he click take the sitting questioner it wil show him his result 
#text in act.html from https://www.juststand.org/the-tools/sitting-time-calculator/ 

from flask import Flask, render_template, request,redirect, url_for, session, g
from database import get_db, close_db
from flask_session import Session
from datetime import datetime, timedelta
from forms import ActivityForm,sportForm, RegistrationForm,LoginForm, appForm, passwordForm
from werkzeug.security import generate_password_hash, check_password_hash  
from functools import wraps
app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.teardown_appcontext
def close_db_at_end_of_request(e =None):
    close_db(e)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/act", methods=["GET", "POST"])
def act():
    form  = ActivityForm()
    totalHours= 0
    dayHours = 0
    if "result" in session:
        result = session["result"]
        del session["result"]
        check_date = datetime.now().date()
        next_check = check_date + timedelta(days=90)
        user_id = session["user_id"]
        db = get_db()
        if db.execute("""SELECT * FROM profile
                    WHERE user_id = ? AND act_result = ?""",(user_id,result)).fetchone() is not None:
            "Result Already in your profile "
        else:
            db.execute("""INSERT INTO profile(user_id, act_result, check_date,next_check)
                VALUES(?,?,?,?);""",(user_id, result, check_date,next_check))
            db.commit()
        return render_template("result.html",result= result, check_date=check_date )
    if form.validate_on_submit():
        eatBH = form.eatBH.data
        eatBM = form.eatBM.data
        travelTH = form.travelTH.data
        travelTM = form.travelTM.data
        workMH = form.workMH.data
        workMM = form.workMM.data
        eatLH = form.eatLH.data
        eatLM = form.eatLM.data
        workAH = form.workAH.data
        workAM = form.workAM.data
        travelBH = form.travelBH.data
        travelBM = form.travelBM.data
        eatDH = form.eatDH.data
        eatDM = form.eatDM.data
        tvH = form.tvH.data
        tvM = form.tvM.data
        computerH = form.computerH.data
        computerM = form.computerM.data
        otherH = form.otherH.data
        otherM = form.otherM.data
        clear = form.clear.data
        exercise = form.exercise.data
        sleep = form.sleep.data
        if exercise == True:
            exercise = 2.5
            dayHours = 24-sleep - exercise
        else:
            dayHours = 24-sleep
        extraHoursFromMin = ( eatBM+ travelTM+ workMM + eatLM + workAM + travelBM+ eatDM + tvM + computerM + otherM)//60
        totalHours =  eatBH  + travelTH + workMH + eatLH + workAH + travelBH + eatDH + tvH + computerH + otherH + extraHoursFromMin
        if clear == True:
            return redirect(url_for("act"))
        if totalHours > dayHours:
            return render_template("act.html",errorMessage = "hours more than 24", form = form)
        else:
            check_date = datetime.now().date()
            next_check = check_date + timedelta(days=30)
            if totalHours < 4:
                result = "LOW risk indicates sitting less than 4 hours per day"
            elif totalHours >= 4 and totalHours< 8:
                result = "MEDIUM risk indicates sitting 4 to 8 hours per day"
            elif totalHours >= 8 and totalHours<= 11:
                result = "HIGH risk indicates sitting 8 to 11 hours per day"
            elif totalHours > 11:
                result = "VERY HIGH risk indicates sitting more than 11 hours per day"
            if "user_id" not in session:
                session["result"] = result
                return redirect(url_for("login", next="act"))
            else:
                user_id = session["user_id"]
                db = get_db()
                if db.execute("""SELECT * FROM profile
                            WHERE user_id = ? AND act_result = ?""",(user_id,result)).fetchone() is not None:
                            pass
                else:
                    db.execute("""INSERT INTO profile(user_id, act_result, check_date,next_check)
                                VALUES(?,?,?,?);""",(user_id, result, check_date,next_check))
                    db.commit()
                    print("WWW")
            return render_template("result.html",result= result, check_date=check_date )
    return render_template("act.html",form = form)


@app.route("/sports", methods=["GET", "POST"])
@login_required
def sports():
    form  = sportForm()
    sports = ''
    if form.validate_on_submit():
        age = form.age.data
        db = get_db()
        sports = db.execute("""SELECT * FROM sports
                            WHERE ? between sport_age_min AND sport_age_max""",(age,)).fetchall()

    return render_template("sport.html",form = form,sports = sports)
@app.route("/appli/<int:sport_id>/<string:sport_name>/<user_id>", methods=["GET", "POST"])
@login_required

def appli(sport_id, sport_name, user_id):
    form = appForm()
    message = ""
    if form.validate_on_submit():
        timeDate = form.timeDate.data
        timeHM = form.timeHM.data
        if timeDate <=  datetime.now().date():
            form.timeDate.errors.append("Date must be in future")
        else:
            db = get_db()
            if db.execute("""SELECT * FROM appointments
                        WHERE sport_id=? AND timeDate = ? AND 
                        timeHM =?""",(sport_id,timeDate,timeHM)).fetchone() is not None:
                form.timeHM.errors.append("Sorry this time is booked, choose another time")
            else:
                db = get_db()
                db.execute("""INSERT INTO appointments(sport_id, sport_name, timeDate,timeHM, user_id)
                                            VALUES(?,?,?,?,?)""",(sport_id, sport_name,timeDate,timeHM, user_id))
                db.commit()
                message = 'Appointment booked for you!'
                return redirect(url_for('profile'))
    return render_template('app.html', message = message,form=form)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user_id"]
    db = get_db()
    user_result_and_date = db.execute("""SELECT * from profile
        WHERE user_id=?""",(user_id,)).fetchall()
    userInfo = db.execute("""SELECT sport_name, timeDate,timeHM,user_id FROM appointments
        WHERE user_id=?""",(user_id,)).fetchall()
    user_full_name = db.execute("""SELECT user_name,user_surname  FROM users
        WHERE user_id=?""",(user_id,)).fetchall()
    return render_template("profile.html", userInfo = userInfo,user_full_name =user_full_name, user_result_and_date = user_result_and_date)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        user_surname = form.user_surname.data
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        if db.execute("""SELECT * FROM users WHERE user_id = ?""",(user_id,)).fetchone() is not None:
            db.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchone()
            form.user_id.errors.append("This username is already used")
        else:
            db.execute("""INSERT INTO users(user_name,user_surname,user_id, password)
                            VALUES (?,?,?,?)""",(user_name,user_surname,user_id, generate_password_hash(password)))
            db.commit()
        return redirect(url_for('login'))
    return render_template("register.html",form = form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute("""SELECT * FROM users
                    WHERE user_id = ?;""", (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("Unknown user id")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("incorrect password!")
        else:
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form = form)


@app.route("/reset", methods=["GET","POST"])
def reset():
    form = passwordForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        oldPassw = form.oldPassw.data
        newPassw = form.newPassw.data
        newPassw2 = form.newPassw2.data
        db = get_db()
        user = db.execute("""SELECT * FROM users
            WHERE user_id = ?;""", (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("Unknown user id")
        else:
            if check_password_hash(user["password"], oldPassw):
                if not newPassw == newPassw2:
                    form.newPassw2.errors.append("Passwords do not match.")
                else:
                    db.execute("""UPDATE users
                                SET password = ?
                                WHERE user_id = ?;""",((generate_password_hash(newPassw)), user_id))
                    db.commit()
                    return redirect(url_for("login"))
            else:
                form.oldPassw.errors.append("incorrect Old password!")
    return render_template("reset.html", form=form)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
