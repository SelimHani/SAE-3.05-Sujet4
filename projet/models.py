from flask_login import UserMixin
from .app import db, login_manager


participer = db.Table('participer',
    db.Column('user_id', db.String(50),
    	db.ForeignKey('user.mail')),
    db.Column('repetition_id', db.Integer,
    	db.ForeignKey('repetition.id'))
)

necessiter = db.Table('necessiter',
    db.Column('repetition_id', db.String(50),
    	db.ForeignKey('repetition.id')),
    db.Column('equipement_id', db.Integer,
    	db.ForeignKey('equipement.id'))
)

exiger = db.Table('exiger',
    db.Column('activite_id', db.String(50),
    	db.ForeignKey('activite.id')),
    db.Column('equipement_id', db.Integer,
    	db.ForeignKey('equipement.id'))
)
    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
    def get_id(self):
        return self.id
    
class Repetition(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    lieu = db.Column(db.String(100))
    date = db.Column(db.String(100))
    description = db.Column(db.String(200))
    equipements = db.relationship("Equipement",secondary=necessiter,backref='repetitions')

class User(db.Model,UserMixin):
    mail = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(200))
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    ddn = db.Column(db.String(100))
    num_tel = db.Column(db.String(10))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref = db.backref("users",lazy="dynamic"))
    repetitions = db.relationship("Repetition",secondary=participer,backref='users')


class Sondage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activite = db.relationship("Activite", uselist=False,backref="sondage") 

class Activite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    lieu = db.Column(db.String(50))
    date = db.Column(db.String(50))
    description = db.Column(db.String(100))
    sondage_id = db.Column(db.Integer, db.ForeignKey("sondage.id"))
    equipements = db.relationship("Equipement",secondary=exiger,backref='activites')

class Equipement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))




@login_manager.user_loader
def load_user(mail): 
    return User.query.get(mail)

def get_roles():
    return Role.query.all()

def get_role_by_id(id):
    return Role.query.get(id)

def get_repetition_by_id(id):
    return Repetition.query.get(id)

def get_roles():
    return Role.query.all()

def get_repetitions():
    return Repetition.query.all()

