from flask_login import UserMixin
from .app import db, login_manager



def get_user(username):
    return User.query.get(username)

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    role = db.Column(db.String(30))

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
