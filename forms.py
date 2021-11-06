from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField,BooleanField,IntegerField,PasswordField,StringField,DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, NumberRange, EqualTo
from decimal import ROUND_HALF_UP

class ActivityForm(FlaskForm):
    eatBH = IntegerField("Eat breakfast Hours:",validators=[InputRequired(),NumberRange(0,24)])
    eatBM = IntegerField("Eat breakfast Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    travelTH = IntegerField("traveling to work/school Hours:",validators=[InputRequired(),NumberRange(0,24)])
    travelTM = IntegerField("traveling to work/school Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    workMH = IntegerField("work[morning] Hours:",validators=[InputRequired(),NumberRange(0,24)])
    workMM = IntegerField("work[morning] Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    eatLH = IntegerField("Eat lunch Hours:",validators=[InputRequired(),NumberRange(0,24)])
    eatLM = IntegerField("Eat lunch Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    workAH = IntegerField("work[Afternoon] Hours:",validators=[InputRequired(),NumberRange(0,24)])
    workAM = IntegerField("work[Afternoon] Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    travelBH = IntegerField("traveling back to home Hours:",validators=[InputRequired(),NumberRange(0,24)])
    travelBM = IntegerField("traveling back to home Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    eatDH = IntegerField("Eat dener Hours:",validators=[InputRequired(),NumberRange(0,24)])
    eatDM = IntegerField("Eat dener Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    tvH = IntegerField("Watch TV/ gaming Hours:",validators=[InputRequired(),NumberRange(0,24)])
    tvM = IntegerField("Watch TV/ gaming Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    computerH = IntegerField("using computer Hours:",validators=[InputRequired(),NumberRange(0,24)])
    computerM = IntegerField("using computer Minutes:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    otherH = IntegerField("Other:",validators=[InputRequired(),NumberRange(0,24)])
    otherM = IntegerField("Other:",validators=[InputRequired(),NumberRange(0,60)],default=0)
    sleep = IntegerField("Sleep Hours:",validators=[InputRequired(),NumberRange(0,24)])
    exercise = BooleanField("Exercise:")
    submit = SubmitField("Calculate")
    clear = SubmitField("clear")

class sportForm(FlaskForm):
    age = IntegerField("Enter your age:",validators=[InputRequired(),NumberRange(2,100)])
    submit = SubmitField("Submit")


class passwordForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    oldPassw = PasswordField("Old password:", validators=[InputRequired()])
    newPassw = PasswordField("new password:", validators=[InputRequired()])
    newPassw2 = PasswordField("new password again:",validators=[InputRequired(),EqualTo("newPassw")])
    submit = SubmitField("Submit")

class appForm(FlaskForm):
    timeDate = DateField("enter a time",validators=[InputRequired()], format='%Y-%m-%d')
    timeHM = SelectField("Select a time that suit you:",
    choices = [("9:00 AM"),
                ("9:30 AM"),
                ("10:00 AM"), 
                ("10:30 AM"), 
                ("12:00 PM"),
                ("12:30 PM"),
                ("01:00 PM"),
                ("02:00 PM"),
                ("02:30 PM"),
                ("03:00 PM"),
                ("03:30 PM"),
                ("04:00 PM"),
                ("04:30 PM"),
                ("05:00 PM")], 
    validators = [InputRequired()])
    #select field with times 
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    user_name = StringField("User Name:", validators=[InputRequired()])
    user_surname = StringField("User Surname:", validators=[InputRequired()])
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Password:",
     validators=[InputRequired(),EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")
