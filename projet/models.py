from flask_login import UserMixin
from .app import db, login_manager


participer = db.Table('participer',
    db.Column('user_id', db.String(50),
    	db.ForeignKey('user.mail')),
    db.Column('repetition_id', db.Integer,
    	db.ForeignKey('repetition.id'))
)

necessiter = db.Table('necessiter',
    db.Column('repetition_id', db.Integer,
    	db.ForeignKey('repetition.id')),
    db.Column('equipement_id', db.Integer,
    	db.ForeignKey('equipement.id'))
)

exiger = db.Table('exiger',
    db.Column('activite_id', db.Integer,
    	db.ForeignKey('activite.id')),
    db.Column('equipement_id', db.Integer,
    	db.ForeignKey('equipement.id'))
)

repondre = db.Table('repondre',
    db.Column('sondage_id', db.Integer,
    	db.ForeignKey('sondage.id')),
    db.Column('reponse_id', db.Integer,
    	db.ForeignKey('reponses_possibles.id'))
)

    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
    def get_name(self):
        return self.name
    
class Repetition(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    lieu = db.Column(db.String(100))
    date = db.Column(db.String(100))
    description = db.Column(db.String(200))
    equipements = db.relationship("Equipement",secondary=necessiter,backref='repetitions')


class Reponse_sondage(db.Model):
    user_id = db.Column(db.String(50), db.ForeignKey('user.mail'), primary_key=True)
    sondage_id = db.Column(db.Integer, db.ForeignKey('sondage.id'), primary_key=True)
    reponse = db.Column(db.String(50))
    user = db.relationship("User", back_populates="sondages")
    sondage = db.relationship("Sondage", back_populates="users")
    
    
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
    sondages = db.relationship("Reponse_sondage", back_populates="user")

    def get_id(self):
        return self.mail

    def get_prenom(self):
        return self.prenom
    
    def get_id_role(self):
        return self.role_id
    
class Sondage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activite = db.relationship("Activite", uselist=False,backref="sondage") 
    users = db.relationship("Reponse_sondage",back_populates="sondage")
    reponses_possibles = db.relationship("Reponses_possibles", secondary=repondre, backref="sondages")
    question = db.Column(db.String(100))
    
    def get_id(self):
        return self.id
    
    def nombre_reponses(self):
        reponses  = Reponse_sondage.query.filter_by(sondage_id=self.id).all()
        repondu = len(reponses)
        musiciens = len(User.query.all())
        return repondu, musiciens
        
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
    
    def get_nom(self):
        return self.nom

class Reponses_possibles(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nom = db.Column(db.String(100))



@login_manager.user_loader
def load_user(mail): 
    return User.query.get(mail)

def get_role_by_id(id):
    return Role.query.get(id)

def get_repetition_by_id(id):
    return Repetition.query.get(id)

def get_roles():
    return Role.query.all()

def get_calendrier():
    a= Activite.query.all()
    b = Repetition.query.all()
    res = a+b
    res = sorted(res,key=lambda item: item.date)
    return res

def get_user_by_id(mail):
    return User.query.get(mail)

def get_equipements():
    return Equipement.query.all()

def get_equipement_by_name(name):
    res=Equipement.query.filter_by(nom=name).first()
    return res

def get_sondages():
    return Sondage.query.all()

def get_sondage_by_id(id):
    return Sondage.query.get(id)

def a_deja_repondu(idu, ids):
    reponse = Reponse_sondage.query.filter_by(user_id=idu, sondage_id=ids).first()
    return reponse is not None

def get_reponses_possibles_by_id(id):
    return Reponses_possibles.query.get(id)

def get_sondage_by_question(question):
    return Sondage.query.filter_by(question=question).first()

def get_reponses_possibles_by_sondage(sondage):
    return sondage.reponses_possibles



