from flask import Flask
from flask_bootstrap import Bootstrap
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = "9d0a186d-85d6-4038-817b-e9461c9a85b7"
bootstrap = Bootstrap(app)
def mkpath(p):
    return os.path.normpath(
        os.path.join(
        os.path.dirname(__file__),
        p))
    
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('./myapp.db'))

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"