from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from school_app.forms import (
    StudentRegistrationForm, 
    StudentLoginForm,
    AdminRegistrationForm,
    AdminLoginForm,
    ComplaintForm
)
from school_app import bcrypt, db
from school_app.models import Student, Admin
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)

# ======================
# STUDENT AUTH ROUTES
# ======================

@auth.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        if hasattr(current_user, 'admin_id'):
            return redirect(url_for('main.admin_dashboard'))
        elif hasattr(current_user, 'student_id'):
            return redirect(url_for('main.student_dashboard'))

    form = StudentRegistrationForm()

    if form.validate_on_submit():
        existing_email = Student.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use another or login.', 'danger')
            return render_template('student_register.html', form=form, title='Student Registration')

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(
            student_names=form.student_names.data,
            student_registration_number=form.student_registration_number.data,
            program=form.program.data,
            department=form.department.data,
            year_of_study=form.year_of_study.data,
            semester=form.semester.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(student)
        db.session.commit()
        flash('Your student account has been created! Please login.', 'success')
        return redirect(url_for('auth.student_login'))

    return render_template('student_register.html', form=form, title='Student Registration')


@auth.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated and isinstance(current_user._get_current_object(), Student):
        return redirect(url_for('main.complaint'))

    form = StudentLoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.complaint'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('student_login.html', form=form, title='Student Login')

# ======================
# ADMIN AUTH ROUTES
# ======================

@auth.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if current_user.is_authenticated:
        if hasattr(current_user, 'admin_id'):
            return redirect(url_for('main.admin_dashboard'))
        elif hasattr(current_user, 'student_id'):
            return redirect(url_for('main.student_dashboard'))

    form = AdminRegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_email = Admin.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use another or login.', 'danger')
            return render_template('admin_register.html', form=form)

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(
            full_name=form.full_name.data,
            username=form.username.data,
            email=form.email.data,
            department=form.department.data,
            password=hashed_password
        )
        db.session.add(admin)
        db.session.commit()
        flash(f'New admin account for {admin.full_name} has been created!', 'success')
        return redirect(url_for('main.admin_dashboard'))

    return render_template('admin_register.html', form=form)



@auth.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and hasattr(current_user, 'admin_id'):
        return redirect(url_for('main.admin_dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            session.pop('_flashes', None)  # Clear any existing flash messages
            return redirect(url_for('main.admin_dashboard'))
        flash('Invalid email or password', 'danger')

    return render_template('admin_login.html', form=form)

# ======================
# GENERAL LOGOUT ROUTE
# ======================

@auth.route('/logout')
@login_required
def logout():
    user = current_user._get_current_object()

    if isinstance(user, Student):
        logout_user()
        flash('You have been logged out as student.', 'info')
        return redirect(url_for('auth.student_login'))

    elif isinstance(user, Admin):
        logout_user()
        flash('You have been logged out as admin.', 'info')
        return redirect(url_for('auth.admin_login'))

    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
