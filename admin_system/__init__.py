'''
Converts the website folder into a python package so that we can export data between files
'''
# Flask is used to create a quick website backend 
from flask import Flask

# Import blueprints
from .route_main import views
from .route_auth import auth

# Import connection variables
from .connections import *



# Create the flask app
def create_app():
  # App configs
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

  # Register the route to access our views ad auth pages
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  return app