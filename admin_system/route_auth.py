'''
This will include all the main routes used for the site
'''
# Blueprint is used to sort our routes
# Render_template is used to render the html pages
# Request is used to get POST data
# Session is used to handle session database_name
# Redirect is used to redirect pages
# Url_for is used to get teh url for a route
# Flash is used to flash success or error messages
from flask import Blueprint, render_template, flash, request, session, redirect, url_for
# import db connection variables
from .connections import *
# authentication functions
from .db_auth import *


# initiate blueprint called "auth"
auth = Blueprint('auth',__name__)


# Create routes
@auth.route('/employee_create', methods=['POST', 'GET'])
def employee_create():
  '''
  Create a route for the employee create page

  Return:
    employee create page
  '''
  
  if request.method == 'POST':
    # request form data
    request_username = request.form['username']
    request_first_name = request.form['first_name']
    request_last_name = request.form['last_name']
    request_email = request.form['email']
    request_phone_number = request.form['phone_number']

    if not request_first_name or not request_last_name or not request_email or not request_phone_number:
      flash('Fill in all personal details before submitting', category='error')
    else:
      user_exist = collection_1.find_one({"employee_login.username": request_username})
      
      if user_exist == None :
        register_user(request_username, request_first_name, request_last_name, request_email, request_phone_number)
        flash('User created!', category='success')
      elif user_exist != None :
        flash('Username already in use', category='error')
      else:
        flash('Error', category='error')
      
  return render_template("details.html", operation = "Create", section= "Employee")


@auth.route('/department_create', methods=['POST', 'GET'])
def department_create():
  '''
  Create a route for the department create page

  Return:
    department create page
  '''
  
  if "user" in session:
    user = "user"
    flash("Access denied", category='error')
    return redirect(url_for('views.home'))
  elif "super_user" in session:
    user = "super_user"
  else:
    flash("You're not logged in", category='error')
    return redirect(url_for('auth.login'))

  # option data
  all_managers = list(collection_1.find({'manager_details.status': True,'admin.status': True}))
  
  if request.method == 'POST':
    # request form data
    request_department = request.form['department']
    request_manager = request.form['manager']

    department_exist = collection_2.find_one({"department_name": request_department})

    if department_exist:
      flash('Department already exist', category='error')
    elif not department_exist:
      if request_manager == "- Select manager -":
        request_manager = None
      flash('Department created', category='success')
      new_department(request_department, request_manager)
    
    
  return render_template("details.html", operation = "Create", section= "Department", user=user, all_managers=all_managers)


@auth.route('/login', methods=['POST', 'GET'])
def login():
  '''
  Create a route for the login page
  
  Return:
    login page
  '''
  if "user" in session:
    flash("User already logged in", category='success')
  elif "super_user" in session:
    flash("Super user already logged in", category='success')
    
  if request.method == 'POST':
    
    # check if logged in already
    if "user" in session:
      flash(f'Logged out of account {session["user"]}.', category='error')
      session.pop("user", None)
    elif "super_user" in session:
      flash(f'Logged out of account {session["super_user"]}.', category='error')
      session.pop("super_user", None)
    
    # request form data
    request_username = request.form['username']
    request_password = request.form['password']

    valid_user = validate_login(request_username, request_password)

    if valid_user == 0:
      flash('Invalid Username!', category='error')
    elif valid_user == 1:
      flash('Invalid Password!', category='error')
    elif valid_user == 2:
      
      # set session timer
      session.permanent = True
      # set session variable
      session["user"] = request_username
      
      
      flash('Welcome Back! You are now logged in', category='success')
      return redirect(url_for('views.home'))
    elif valid_user == 3:
      # set session timer
      session.permanent = True
      # set session variable
      session["super_user"] = request_username
  
      flash('Logged in as super user', category='success')
      return redirect(url_for('views.home'))
    else:
      return valid_user
    
    
  return render_template("login.html")


@auth.route('/logout')
def logout():
  '''
  Create a route for logging out

  Return:
    logout page
  '''
  if "user" in session:
    flash(f'Logged out of account {session["user"]}.', category='error')
    #remove session data
    session.pop("user", None)
    return redirect(url_for('auth.login'))
  elif "super_user" in session:
    flash(f'Logged out of account {session["super_user"]}.', category='error')
    #remove session data
    session.pop("super_user", None)
    return redirect(url_for('auth.login'))
  else:
    flash("You're not logged in", category='error')
    return redirect(url_for('auth.login'))