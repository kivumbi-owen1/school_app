from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from school_app.models import Student, Admin

# ======================
# STUDENT FORMS
# ======================

class StudentRegistrationForm(FlaskForm):
    student_names = StringField('Full Names', validators=[
        DataRequired(), 
        Length(min=1, max=150)
    ])
    student_registration_number = StringField('Registration Number', validators=[
        DataRequired(), 
        Length(min=1, max=150)
    ])
    program = StringField('Program', validators=[
        DataRequired(), 
        Length(min=1, max=100)
    ])
    department = StringField('Department', validators=[
        DataRequired(), 
        Length(min=1, max=100)
    ])
    year_of_study = StringField('Year of Study', validators=[
        DataRequired(), 
        Length(min=1, max=100)
    ])
    semester = StringField('Semester', validators=[
        DataRequired(), 
        Length(min=1, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(), 
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, max=100)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')
    ])
    submit = SubmitField('Register as Student')


class StudentLoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login as Student')

# ======================
# ADMIN FORMS
# ======================

class AdminRegistrationForm(FlaskForm):
    full_name = StringField('Full Names', validators=[
        DataRequired(), 
        Length(min=1, max=150)
    ])
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(), 
        Length(max=100)
    ])
    department = StringField('Department', validators=[
        DataRequired(), 
        Length(min=1, max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, max=100)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')
    ])
    submit = SubmitField('Register as Admin')

class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login as Admin')

# ======================
# COMPLAINT FORM
# ======================

class ComplaintForm(FlaskForm):
    course_name = StringField('Course Unit Name', validators=[
        DataRequired(), 
        Length(max=120)
    ])
    course_code = StringField('Course Code', validators=[
        DataRequired(), 
        Length(max=120)
    ])
    course_intake = StringField('Course Intake', validators=[
        DataRequired(), 
        Length(max=120)
    ])
    complaint_text = TextAreaField('Complaint Details', validators=[
        DataRequired(), 
        Length(min=10, max=500)
    ])
    lecturer_names = StringField('Lecturer Name(s)', validators=[
        DataRequired(), 
        Length(max=120)
    ])
    lecturer_email = StringField('Lecturer Email', validators=[
        DataRequired(), 
        Email(), 
        Length(max=120)
    ])
    submit = SubmitField('Submit Complaint')