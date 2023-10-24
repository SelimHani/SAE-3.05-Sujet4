from flask_login import UserMixin
from .app import db, login_manager


class User(db.Model,UserMixin):
    mail = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(30))
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    ddn = db.Column(db.String(100))
    num_tel = db.Column(db.String(10))
    
    def get_id(self):
        return self.mail

@login_manager.user_loader
def load_user(mail):
    return User.query.get(mail)