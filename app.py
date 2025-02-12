from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the secret key for session management
app.config['SECRET_KEY'] = 'M!@#$t33178250'

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'

# Disable SQLAlchemy modification tracking to reduce memory usage
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the upload folder for profile pictures
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pictures')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize the database object
db = SQLAlchemy(app)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect unauthenticated users to the login page
login_manager.login_message_category = 'info'  # Set a Bootstrap-compatible message category

# Define the user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User  # Avoid circular import by importing here
    return User.query.get(int(user_id))

# Import routes after initializing app and db to avoid circular imports
from routes import *

if __name__ == '__main__':
    # Run the application in debug mode during development
    app.run(debug=True)