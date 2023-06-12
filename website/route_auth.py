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
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
# import main CRUD functions
from.db_main import *
# authentication functions
from .db_auth import *
# import db connection variables
from .connections import *


# initiate blueprint called "auth"
auth = Blueprint('auth',__name__)


# Create routes
@auth.route('/signup', methods=['POST', 'GET'])
def signup():
  '''
  Create a route for the signup page

  GET method:
    display sign up page

  POST method:
    send necessary fields needed to sign up (name, username, email, password)

  Return:
    valid = 0 if user not in database
      sign up new user
      redirects to home page
    valid = 1 if user is in database but incorrect password
      flash incorrect password
    valid = 2 if correct user an correct password
      login user
      redirects to home page
  '''
  
  if "username" in session:
      flash("You're already logged in", category='success')

  if request.method == 'POST':
    # request form data
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirmed_password = request.form['confirm_password']

    # check if user exist
    valid_user = validate_login(username, password)
    
    # check valid email
    valid_email = email_validation(email)
    
    # check password and confirmed password
    if password == confirmed_password:
      valid_password = True
    else:
      valid_password = False
    
    if valid_email: # valid email layer
      if valid_password: # valid password match layer
        if valid_user == 0:
          
          # set session timer
          session.permanent = True
          #set session variable
          session["username"] = username
          
          # register new user in MongoDB
          register_user(name=name, username=username, email=email, password=password)
          flash('Successful Sign Up!', category='success')
          return redirect(url_for('views.home'))
        elif valid_user == 1:
          flash('Username Already Exist', category='error')
        elif valid_user == 2:
          
          # set session timer
          session.permanent = True
          #set session variable
          session["username"] = username
          
          flash('Welcome Back! You are now logged in', category='success')
          return redirect(url_for('views.home'))
        else:
          return valid_user
      else:
        flash('Please make sure passwords match!', category='error')
    else:
      flash('Please enter valid email address', category='error')
  return render_template("signup.html", logged_in=current_user.is_authenticated)
  


@auth.route('/login', methods=['POST', 'GET'])
def login():
  '''
  Create a route for the login page

  GET method:
    display login page

  POST method:
    send necessary fields needed to login (username & password)

  Return:
    valid = 0 if user not in database
      flash incorrect user
    valid = 1 if user is in database but incorrect password
      flash incorrect password
    valid = 2 if correct user an correct password
      login user
      redirects to home page
  '''
  
  if "username" in session:
    flash("You're already logged in", category='success')
  
  if request.method == 'POST':
    # request form data
    username = request.form['username']
    password = request.form['password']
    
    # check if user exist
    valid_user = validate_login(username, password)

    if valid_user == 0:
      flash('Invalid Username!', category='error')
    elif valid_user == 1:
      flash('Invalid Password!', category='error')
    elif valid_user == 2:
      
      # set session timer
      session.permanent = True
      #set session variable
      session["username"] = username
      
      flash('Welcome Back! You are now logged in', category='success')
      return redirect(url_for('views.home'))
    else:
      return valid_user
  return render_template("login.html", logged_in=current_user.is_authenticated)

@auth.route('/logout')
def logout():
  '''
  Create a route for logging out

  Return:
    flash logout message
    redirect to login page
  '''
  if "username" in session:
    flash(f'Logged out {session["username"]}.', category='error')

    #remove session data
    session.pop("username", None)
    
    return redirect(url_for('auth.login'))
  else:
    flash("You're not logged in", category='error')
    return redirect(url_for('auth.login'))