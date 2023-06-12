'''
CRUD functions related to the user collection
'''
# import db connection variables
from .connections import *
# import main CRUD functions
from.db_main import *
# hashing user password
import bcrypt
# valid email
from validate_email import validate_email
# manage session data 
from flask import session
# timer
from datetime import timedelta


# Log manager
from flask_login import login_user, logout_user, login_required , current_user

# USER HELPER FUNCTIONS ---------------------------------------------------------------

def hash_password(password: str) -> bytes:
  '''
  Hashes a password string and returns it in bytes form
  
  Args:
    password (str): password in string format
  
  Return:
    byte version of hashed password
  '''
  return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def email_validation(email: str) -> bool:
  '''
  Check if email address is valid

  Args:
    email (str): user email
  
  Return:
    True - if valid email
    False - otherwise
  '''
  try:
    valid_email = validate_email(email, verify=True)
    if valid_email:
      return True
    else: 
      return False
  except Exception as e:
    return e


# NEW USER ---------------------------------------------------------------------------

def register_user(name: str, username: str, email: str, password: str) -> bool:
  """
  Register a new user
  
  Args:
    name (str): name of new user
    username (str): new user account name
    email (str): new user's email address
    password (str): new user's password
  
  Return:
    True - if user was successfully registered
    False - otherwise
  """
  hashpassword = hash_password(password)
  new_user = {
      "name": name,
      "username": username,
      "email": email,
      "password": hashpassword
    }
  try:
    add_item(collection_2, new_user)
    print('user added to database')
    return True
  except Exception:
    return False


# FIND USER ---------------------------------------------------------------------------

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
  '''

  try:
    user_exist = collection_2.find_one({'username': username })
    
    if user_exist == None :
      return 0
    elif user_exist != None:
      hashpassword = password.encode("utf-8")
      correct_password = bcrypt.checkpw(hashpassword, user_exist['password'])
      if correct_password == False:
        return 1
      else:
        return 2
  except Exception as e:
    return e


# UPDATE USER -------------------------------------------------------------------------

def update_user(username: str, doc: dict) -> bool:
  '''
  update user details

  Args:
    username (str): username of account
    doc (dict): dictionary of updated details

  Return:
    True - if user details were successfully updated
    False - otherwise
  '''
  pass

# REMOVE USER -------------------------------------------------------------------------

def remove_user(username: str) -> bool:
  '''
  delete a item
  
  Args:
    username (str): username to be deleted

  Return:
    True - if user was successfully deleted
    False - otherwise
  '''
  collection_2.delete_one({"username": username})
  return username