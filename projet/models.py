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




sond = db.Table("sond", db.Column('sondage_id', db.Integer, db.ForeignKey('sondage.idSondage'), primary_key=True),
        db.Column('activiter_id', db.Integer, db.ForeignKey('activiter.idActiviter'), primary_key=True)     )


class Sondage(db.Model):
    idSondage = db.Column(db.Integer, primary_key=True)
    Jour = db.Column(db.String(100))

    act_id = db.relationship("Activiter", secondary = sond)   


class Activiter(db.Model):
    idActiviter = db.Column(db.Integer, primary_key=True)
    nomAct = db.Column(db.String(50))
    lieuAct = db.Column(db.String(50))
    date = db.Column(db.String(50))
    description = db.Column(db.String(50))
    
    equipement_id = db.Column(db.Integer, db.ForeignKey('equipement.idEquipement'))
    equipement = db.relationship("Equipement",backref= db.backref("equipements",lazy="dynamics"))

    sond_id = db.relationship("Sondage", secondary = sond)

class Equipement(db.Model):
    idEquipement = db.Column(db.Integer, primary_key=True)
    nomEquipement = db.Column(db.String(100))




@login_manager.user_loader
def load_user(mail):
    return User.query.get(mail)