from flask_login import UserMixin
from .app import db, login_manager
from sqlalchemy import func
from datetime import datetime

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
    

class Proche(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    proche_mail = db.Column(db.String(50), db.ForeignKey('user.mail'))
    musicien_mail = db.Column(db.String(50), db.ForeignKey('user.mail'))
    user = db.relationship("User", foreign_keys=[musicien_mail], backref='proche_of')
    proche = db.relationship("User", foreign_keys=[proche_mail], backref='proches')


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
    date_fin = db.Column(db.String(100))
    
    def get_id(self):
        return self.id
    
    def nombre_reponses(self):
        reponses  = Reponse_sondage.query.filter_by(sondage_id=self.id).all()
        repondu = len(reponses)
        musiciens = len(User.query.filter_by(role_id=1).all())
        return repondu, musiciens
    

    def get_pourcentage_rep(self):
        personne =Reponse_sondage.query.filter_by(sondage_id=self.id).with_entities(Reponse_sondage.user_id, Reponse_sondage.reponse).all()
        reponses_possibless = {elem.nom: 0 for elem in Sondage.query.get(self.id).reponses_possibles}
        per = len(personne)
        for elem in personne:
            type = Reponses_possibles.query.get(elem[1]).nom
            if type in reponses_possibless.keys():
                reponses_possibless[type] += 1
        return reponses_possibless

    def get_date(self):
        return self.date_fin
    
    def jours_restants(self):
        date_fin = datetime.strptime(self.date_fin, '%Y-%m-%d')  # Convertir la chaîne en objet datetime
        aujourdhui = datetime.now()  # Date actuelle

        difference = date_fin - aujourdhui  # Calcul de la différence de dates
        return difference.days  # Nombre de jours restants jusqu'à la date de fin

        
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
    a= Activite.query.filter(Activite.date >= func.now()).all()
    b= Repetition.query.filter(Repetition.date >= func.now()).all()
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
    s = Sondage.query.filter(Sondage.date_fin >=func.now()).all()
    return sorted(s,key=lambda item: item.date_fin,reverse=True)

def get_sondages_finis(): 
    s = Sondage.query.filter(Sondage.date_fin <=func.now()).all()
    return sorted(s,key=lambda item: item.date_fin,reverse=True)

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

def get_musiciens_repetition(id):
    r = Repetition.query.get(id)
    r = r.users
    res = sorted(r,key=lambda item: item.nom)
    return res

def get_musiciens_pas_repetition(id):
    r= User.query.filter(~User.repetitions.any(Repetition.id ==id)).filter(User.role_id==1).all()
    res = sorted(r,key=lambda item: item.nom)
    return res