# add views (endpoints) in employee_management/EmployeeViews.py
from flask import Blueprint, render_template
from flask_login import login_required
employee_app = Blueprint('employee_management', __name__)


@employee_app.route('/employee')
@login_required
def employeeView():
    return 'employee_management'


@employee_app.route("/about", methods=['GET', 'POST'])
@login_required
def aboutUs():
    return render_template('about.html')


@employee_app.route("/contact", methods=['GET', 'POST'])
@login_required
def contactUs():
    return render_template('contact.html')


@employee_app.route("/register", methods=['GET', 'POST'])
@login_required
def employees():
    return render_template('form.html')
