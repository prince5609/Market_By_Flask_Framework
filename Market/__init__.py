from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Market.db"
app.config["SECRET_KEY"] = '61c332e2cd25a2477f8f6aa0'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = "Please LogIn To Access To Market"
login_manager.login_message_category = "info"
from Market import Routes
