from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)  # Initialize the login manager
login_manager.login_view = 'login'  # Set the login view for redirection

# Import routes after initializing app and db
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
