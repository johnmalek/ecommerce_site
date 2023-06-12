'''
Converts the website folder into a python package so that we can export data between files
'''
# Flask is used to create a quick website backend 
from flask import Flask
from flask_login import LoginManager
login_manager = LoginManager()
# timer
from datetime import timedelta

# Import blueprints
from .route_main import views
from .route_auth import auth

# Import connection variables
from .connections import *

@login_manager.user_loader
def load_user(user_id):
    return collection_2.get(user_id)

# Create the flask app
def create_app():
  # App configs
  app = Flask(__name__)
  app.config['SECRET_KEY'] = "ThisisatestsecretkeyIwillchangeitlater"
  login_manager.init_app(app)
  # set timer for session data
  app.permanent_session_lifetime = timedelta(days=3)

  # Register the route to access our views ad auth pages
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  return app