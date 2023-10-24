from flask_login import UserMixin
from .app import db, login_manager


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    

class User(db.Model,UserMixin):
    mail = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(200))
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    ddn = db.Column(db.String(100))
    num_tel = db.Column(db.String(10))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref = db.backref("users",lazy="dynamic"))
    
    def get_id(self):
        return self.mail
    


@login_manager.user_loader
def load_user(mail):
    return User.query.get(mail)


def get_role_by_id(id):
    return Role.query.get(id)