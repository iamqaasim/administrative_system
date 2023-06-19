'''
CRUD functions related to the user collection
'''
# import db connection variables
from .connections import *
# hashing user password
import bcrypt
# import main CRUD functions
from.db_main import *


# USER ---------------------------------------------------------------------------

def hash_password(password: str) -> bytes:
  '''
  Hashes a password string and returns it in bytes form
  
  Args:
    password (str): password in string format
  
  Return:
    byte version of hashed password
  '''
  passwd = password.encode('utf-8')
  return bcrypt.hashpw(passwd, bcrypt.gensalt())


def register_user(username: str, first_name: str, last_name: str, email: str, phone: int) -> bool:
  """
  Register a new user
  
  Args:
    username (str): username
    first_name (str): name of new user
    last_name (str): surname of new user
    email (str): new user's email address
    phone (int): new user's phone number
  
  Return:
    True - if user was successfully registered
    False - otherwise
  """
  
  hashpassword = hash_password("Password123#")
  
  new_user = {
      "employee_details":{
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "current_manager": None,
        "current_department": None,
      },
      "employee_login":{
        "username": username,
        "password": hashpassword,
      },
      "admin": {
        "status": False,
        "managers": [],
        "departments": [],
      },
      "manager_details": {
        "status": False,
        "departments": [],
      }
    }
  try:
    add_item(collection_1, new_user)
    print(" ")
    print('new user added to database')
    print(" ")
    return True
  except Exception as e:
    print(" ")
    print(e)
    print('new user NOT added to database')
    print(" ")
    return False


def validate_login(username: str, password: str):
  '''
  Used for verification in login and signup process
  
  Validate 
    if user exist, 
    if user password is correct

  Args:
    username (str): username 
    password (str): user's password

  Return:
    0 if user not in database
    1 if user is in database but incorrect password
    2 if correct user an correct password
    3 if super user
  '''

  if  username == "hradmin@test.com" and password == "TestPass1234":
    return 3
          
  try:
    user_exist = collection_1.find_one({"employee_login.username": username})
    print(" ")
    print(user_exist)
    if user_exist == None :
      return 0
    elif user_exist != None:
      hashpassword = password.encode("utf-8")
      print(hashpassword)
      correct_password = bcrypt.checkpw(hashpassword, user_exist['employee_login']['password'])
      print(correct_password)
      print(" ")
      if correct_password == False:
        return 1
      else:
        return 2
  except Exception as e:
    print(e)
    print(" ")
    return e


def update_user(username: str, first_name: str, last_name: str, email: str, phone: int) -> bool:
  """
  update user personal details
  
  Args:
    username (str): username of employee
    first_name (str): name of new user
    last_name (str): surname of new user
    email (str): user's email address
    phone (int): user's phone number

  Return:
    True - if user was successfully updated
    False - otherwise
  """          
  
  user_exist = collection_1.find_one({"employee_login.username": username})
  print(" ")
  print(user_exist)
  
  updates = {
    "$set": {
      "employee_details":{
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "current_manager": user_exist['employee_details']['current_manager'],
        "current_department": user_exist['employee_details']['current_department'],
      },
      "employee_login":{
        "username": user_exist['employee_login']['username'],
        "password": user_exist['employee_login']['password'],
      },
      "admin": {
        "status": user_exist['admin']['status'],
        "managers": user_exist['admin']['managers'],
        "departments": user_exist['admin']['departments'],
      },
      "manager_details": {
        "status": user_exist['manager_details']['status'],
        "departments": user_exist['manager_details']['departments'],
      }
    }
  }
    
  try:
    collection_1.update_one({"employee_login.username": username}, updates)
    print(" ")
    print('user personal details updated')
    print(" ")
    return True
  except Exception as e:
    print(" ")
    print(e)
    print('user personal details NOT updated')
    print(" ")
    return False


def admin_update_user(username: str, title: str, department: str, manager: str, status: str) -> bool:
  """
  update existing users admin details
  
  Args:
    username (str): username of employee
    title (str): employee or manager
    department (str): users departments
    manager (str): users managers 
    status (str): users status
  
  Return:
    True - if user was successfully updated
    False - otherwise
  """
  
  user_exist = collection_1.find_one({"employee_login.username": username})

  #check employee title
  if title == "- Select title -":
    title = user_exist['manager_details']['status']
  if title == "Manager":
    title = True
  elif title == "Employee":
    title = False

  if status == '- Select status -':
    status_update = user_exist['admin']['status']
  if status == 'active':
    status_update = True
  elif status == 'inactive':
    status_update = False

    
  if title == True: # indicating that this is a manager
    
    # set manger details
    current_departments_managing = user_exist['manager_details']['departments']

    if department == '- Select department -':
      departments_managing = current_departments_managing
    elif department in current_departments_managing:
      departments_managing = current_departments_managing
    else:
      current_departments_managing.append(department)
      departments_managing = current_departments_managing
  
    manager_details_update = {
      "$set": {
        "employee_details":{
          "first_name": user_exist['employee_details']['first_name'],
          "last_name": user_exist['employee_details']['last_name'],
          "email": user_exist['employee_details']['email'],
          "phone": user_exist['employee_details']['phone'],
          "current_manager": None,
          "current_department": None,
        },
        "employee_login":{
          "username": user_exist['employee_login']['username'],
          "password": user_exist['employee_login']['password'],
        },
        "admin": {
          "status": status_update,
          "managers": [],
          "departments": [],
        },
        "manager_details": {
          "status": True,
          "departments": departments_managing,
        }
      }
    }
    
    try:
      collection_1.update_one({"employee_login.username": username}, manager_details_update)
      print(" ")
      print('user admin manager details updated')
      print(" ")
      return True
    except Exception as e:
      print(" ")
      print(e)
      print('user admin manager details NOT updated')
      print(" ")
      return False
      
  elif title == False: # indictaing this is an employee
    
    current_managers_list = user_exist['admin']['managers']
    current_departments_list = user_exist['admin']['departments']

    if manager == "- Select manager -":
      manager = None
      managers_list = current_managers_list
      manager = user_exist['employee_details']['current_manager']
    elif manager in current_managers_list:
      managers_list = current_managers_list
    elif manager not in current_managers_list:
      current_managers_list.append(manager)
      managers_list = current_managers_list

    if department == "- Select department -":
      department = None
      departments_list = current_departments_list
      department = user_exist['employee_details']['current_department']
    elif department in current_departments_list:
      departments_list = current_departments_list
    elif department not in current_departments_list:
      current_departments_list.append(department)
      departments_list = current_departments_list
    
    
    employee_details_update = {
      "$set": {
        "employee_details":{
          "first_name": user_exist['employee_details']['first_name'],
          "last_name": user_exist['employee_details']['last_name'],
          "email": user_exist['employee_details']['email'],
          "phone": user_exist['employee_details']['phone'],
          "current_manager": manager,
          "current_department": department,
        },
        "employee_login":{
          "username": user_exist['employee_login']['username'],
          "password": user_exist['employee_login']['password'],
        },
        "admin": {
          "status": status_update,
          "managers": managers_list,
          "departments": departments_list,
        },
        "manager_details": {
          "status": False,
          "departments": [],
        }
      }
    }

    try:
      collection_1.update_one({"employee_login.username": username}, employee_details_update)
      print(" ")
      print('user admin employee details updated')
      print(" ")
      return True
    except Exception as e:
      print(" ")
      print(e)
      print('user admin employee details NOT updated')
      print(" ")
      return False


def employee_list_data(department: str, status: str, manager: str):
  """
  get employee list data
  
  Args:
    department (str): departments query
    status (str): status query
    manager (str): logged in manager
    
  Return:
    True - if user was successfully updated
    False - otherwise
  """

  if status == '- Select status -':
    status_query = True
  if status == 'active':
    status_query = True
  elif status == 'inactive':
    status_query = False

  if department == "- Select department -":
    department = None

  
  data = collection_1.find({'employee_details.current_department': department, 'employee_details.current_manager': manager, 'admin.status': status_query })
  
  return list(data)


def admin_employee_list_data(department: str, status: str, manager: str):
  """
  get employee list data
  
  Args:
    department (str): departments query
    status (str): status query
    manager (str): manager query
  
  Return:
    True - if user was successfully updated
    False - otherwise
  """
  
  if status == '- Select status -':
    status_query = True
  if status == 'active':
    status_query = True
  elif status == 'inactive':
    status_query = False

  if department == "- Select department -":
    department = None

  if manager == "- Select manager -":
    manager = None
  
  data = collection_1.find({'employee_details.current_department': department, 'admin.status': status_query, 'employee_details.current_manager': manager })
  
  return list(data)
# DEPARTMENT ---------------------------------------------------------------------------

def new_department(department: str, manager: str) -> bool:
  """
  Register a new user
  
  Args:
    department (str): name of new department
    manager (str): users manager
  
  Return:
    True - if user was successfully registered
    False - otherwise
  """

  new_department = {
      "department_name": department,
      "manager": manager,
      "status": False
    }
  try:
    add_item(collection_2, new_department)
    print(" ")
    print('new department added to database')
    print(" ")
    return True
  except Exception as e:
    print(" ")
    print(e)
    print('new department NOT added to database')
    print(" ")
    return False

    
def update_department(department: str, manager: str, status: bool) -> bool:
  """
  Register a new user
  
  Args:
    department (str): name of new department
    manager (str): users manager
    status (bool): active or inactive department
  
  Return:
    True - if user was successfully registered
    False - otherwise
  """
  department_exist = collection_2.find_one({"department_name": department})
  
  if status == '- Select status -':
    status_update = department_exist['status']
  if status == 'active':
    status_update = True
  elif status == 'inactive':
    status_update = False

  if manager == "- Select manager -":
      manager = department_exist['manager']
  
  
  updates = {
    "$set": {
      "department_name": department,
      "manager": manager,
      "status": status_update,
    }
  }
  try:
    collection_2.update_one({"department_name": department}, updates)
    print(" ")
    print('department updated')
    print(" ")
    return True
  except Exception as e:
    print(" ")
    print(e)
    print('department NOT updated')
    print(" ")
    return False