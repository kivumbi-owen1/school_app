from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from school_app.models import Complaint, Student, Admin
from school_app.forms import ComplaintForm
from school_app import db
from flask_login import current_user, login_required, logout_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        if hasattr(current_user, 'admin_id'):
            return redirect(url_for('main.admin_dashboard'))
        elif hasattr(current_user, 'student_id'):
            return redirect(url_for('main.student_dashboard'))
    return render_template('landing.html')

@main.route('/complaint', methods=['GET', 'POST'])
@login_required
def complaint():
    # Verify student status
    if not hasattr(current_user, 'student_id'):
        logout_user()
        flash('Please login as student to continue', 'danger')
        return redirect(url_for('auth.student_login'))

    form = ComplaintForm()
    if form.validate_on_submit():
        new_complaint = Complaint(
            student_id=current_user.student_id,
            course_name=form.course_name.data,
            course_code=form.course_code.data,
            course_intake=form.course_intake.data,
            complaint_text=form.complaint_text.data,
            lecturer_names=form.lecturer_names.data,
            lecturer_email=form.lecturer_email.data,
        )
        
        db.session.add(new_complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('main.complaint'))  # Redirect back to clear form
    
    return render_template('complaints.html', form=form, title='Submit Complaint')

@main.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.home'))

    query = request.args.get('query', '').strip()
    if query:
        complaints = db.session.query(Complaint, Student).join(Student).filter(
            (Student.student_names.ilike(f"%{query}%")) |
            (Student.student_registration_number.ilike(f"%{query}%")) |
            (Complaint.course_name.ilike(f"%{query}%")) |
            (Complaint.course_code.ilike(f"%{query}%"))
        ).order_by(Complaint.date_filed.desc()).all()
    else:
        complaints = db.session.query(Complaint, Student).join(Student).order_by(Complaint.date_filed.desc()).all()

    # unpack tuples: Complaint + Student
    complaint_data = []
    for complaint, student in complaints:
        complaint.student_names = student.student_names
        complaint.student_registration_number = student.student_registration_number
        complaint_data.append(complaint)

    return render_template('admin_dashboard.html', complaints=complaint_data)

@main.route('/student/dashboard')
@login_required
def student_dashboard():
    # Ensure only students can access this route
    if not isinstance(current_user._get_current_object(), Student):
        flash('Access denied. Student account required.', 'danger')
        return redirect(url_for('main.home'))
    
    # Get the student's recent complaints (last 3)
    recent_complaints = Complaint.query.filter_by(student_id=current_user.student_id)\
                                     .order_by(Complaint.date_filed.desc())\
                                     .limit(3)\
                                     .all()
    
    # Count total complaints
    total_complaints = Complaint.query.filter_by(student_id=current_user.student_id).count()
    
    # Count resolved complaints (you'll need to add a status field to your Complaint model)
    # resolved_complaints = Complaint.query.filter_by(student_id=current_user.student_id, status='resolved').count()
    # For now we'll use placeholder values
    
    return render_template('student_dashboard.html',
                         recent_complaints=recent_complaints,
                         total_complaints=total_complaints)

@main.route('/register/options')
def register_options():
    if current_user.is_authenticated:
        if hasattr(current_user, 'admin_id'):
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.home'))
    return render_template('register_options.html')

@main.route('/login/options')
def login_options():
    if current_user.is_authenticated:
        if hasattr(current_user, 'admin_id'):
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.home'))
    return render_template('login_options.html')