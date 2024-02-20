import click
from .app import app, db
from .models import *
from hashlib import sha256
import os


@app.cli.command()
def syncdb():
    db.create_all()
    
@app.cli.command()
def delete_db():
    if os.path.exists('./myapp.db'):
        os.remove('./myapp.db')
        
        
@app.cli.command()
def loadbd():
    if os.path.exists('./myapp.db'):
        os.remove('./myapp.db')
    db.create_all()
    r1 = Role(id=1, name="Musicien")
    r2 = Role(id=2, name="Directrice")
    r3 = Role(id=3, name="Responsable")
    r4 = Role(id=4, name="Proche")

    e1 = Equipement(id=1, nom="Costume")
    e2 = Equipement(id=2, nom="Piano")
    e3 = Equipement(id=3, nom="Violon")
    e4 = Equipement(id=4, nom="Flute")
    e5 = Equipement(id=5, nom="Clarinette")
    e6 = Equipement(id=6, nom="Tambour")

    re1 = Reponses_possibles(id=1, nom= "JE PARTICIPE")
    re2 = Reponses_possibles(id=2, nom="JE NE PARTICIPE PAS")
    re3 = Reponses_possibles(id=3, nom="OUI")
    re4 = Reponses_possibles(id=4, nom="NON")
    re5 = Reponses_possibles(id=5, nom="PEUT ETRE")
    re6 = Reponses_possibles(id=6, nom="VENTS")
    re7 = Reponses_possibles(id=7, nom="CUIVRES")
    re8 = Reponses_possibles(id=8, nom="PERSCUSSIONS")
    re9 = Reponses_possibles(id=9, nom="CORDES")

    admin = User(mail = "admin@gmail.com", password=sha256("admin".encode()).hexdigest(),num_tel="0871661865", role_id=3, nom="admin", prenom="admin")
    
    user1 = User(mail = "a@gmail.com", password = sha256("a".encode()).hexdigest(),num_tel="0871661865",nom = "Poulet", prenom="Jule", role_id = 1)
    user1000 = User(mail = "aaa@gmail.com", password = sha256("ab".encode()).hexdigest(),num_tel="0871661865",nom = "Leba", prenom="let", role_id = 4)

    proche1 = Proche(id=1, musicien_mail ="a@gmail.com", proche_mail = "aaa@gmail.com")

    user2 = User(mail = "b@gmail.com", password = sha256("b".encode()).hexdigest(),num_tel="0871661865",nom = "Monton", prenom="Christophe", role_id = 1)
    user3 = User(mail = "c@gmail.com", password = sha256("c".encode()).hexdigest(),num_tel="0871661865",nom = "Doe", prenom="John", role_id = 1)
    user4 = User(mail = "d@gmail.com", password = sha256("d".encode()).hexdigest(),num_tel="0871661865",nom = "Joie", prenom="Marie", role_id = 1)
    user5 = User(mail = "e@gmail.com", password = sha256("e".encode()).hexdigest(),num_tel="0871661865",nom = "Laguitare", prenom="Joe", role_id = 1)
    user6 = User(mail = "f@gmail.com", password = sha256("f".encode()).hexdigest(),num_tel="0871661865",nom = "Tou", prenom="Emma", role_id = 1)
    user7 = User(mail = "g@gmail.com", password = sha256("g".encode()).hexdigest(),num_tel="0871661865",nom = "Macron", prenom="Emmanuel", role_id = 1)
    
    r1 = Repetition(id=1, lieu="gymnase Mozart",date="2023-10-11",equipements=[e1,e2], description="repetition des percussions")
    r2 = Repetition(id=2, lieu="gymnase Mozart",date="2024-02-10",equipements=[e1,e2,e4], description="repetition des instruments à vents")
    r3 = Repetition(id=3, lieu="18 rue des cuivres",date="2022-08-22",equipements=[e3,e5], description="repetition des violons et clarinette")
    r4 = Repetition(id=4, lieu="gymnase Mozart",date="2023-10-01",equipements=[e1,e6], description="repetition orchestre")
    r5 = Repetition(id=5, lieu="10 boulevard Bethoven",date="2023-12-22",equipements=[e1,e2,e3,e4,e5], description="repetition avant le concert de noel")
    
    a1 = Activite(id=1, nom="Concert de Noel", lieu="salle des fêtes",date="2023-12-24",equipements=[e1,e2,e3,e4,e5,e6],description="concert de noel avec tout l'orchestre")
    a2 = Activite(id=2, nom="Orchestre", lieu="studio Hollywood",date="2024-03-12",equipements=[e1,e2,e3,e4,e5,e6],description="orchestre pour film à Hollywood")
    a3 = Activite(id=3, nom="Concert de des percussions", lieu="gymnase sportif",date="2023-12-28",equipements=[e6],description="concert de tambour, batterie, triangle")
    a4 = Activite(id=4, nom="Carnaval", lieu="salle des fêtes",date="2024-01-20",equipements=[e1,e2,e3,e4],description="défilé carnaval depart salle des fêtes")
    
    s1= Sondage(id=1, activite=a1, reponses_possibles=[re1,re2],date_fin ="2023-12-23")
    s2= Sondage(id=2, activite=a2, reponses_possibles=[re1,re2],date_fin ="2024-01-20")
    s3= Sondage(id=3, activite=a3, reponses_possibles=[re1,re2],date_fin ="2023-12-30")
    s4= Sondage(id=4, activite=a4, reponses_possibles=[re1,re2],date_fin ="2024-01-10")
    
    s5= Sondage(id=5, question="Etes-vous satisfait de notre application web", reponses_possibles=[re3,re4,re5],date_fin ="2023-12-24")
    s6= Sondage(id=6, question="Quel est votre famille d'instruments favorite?", reponses_possibles=[re6,re7,re8,re9],date_fin ="2024-01-01")
    
    db.session.add(user1)
    db.session.add(user1000)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(r4)
    db.session.add(r5)
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.add(a4)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    db.session.add(s6)
    db.session.add(re1)
    db.session.add(re2)
    db.session.add(re3)
    db.session.add(re4)
    db.session.add(re5)
    db.session.add(re6)
    db.session.add(re7)
    db.session.add(re8)
    db.session.add(re9)
    db.session.add(e1)
    db.session.add(e2)
    db.session.add(e3)
    db.session.add(e4)
    db.session.add(e5)
    db.session.add(e6)
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(admin)
    db.session.add(proche1)
    db.session.commit()

@app.cli.command()
@click.argument("username")
@click.argument("password")
@click.argument("role")
def newuser(username, password, role):
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest(), role=role)
    db.session.add(u)
    db.session.commit()



@app.cli.command()
@click.argument("id")
@click.argument("name")
def newrole(id, name):
    from .models import Role

    u=Role(id=id, name=name)
    db.session.add(u)
    db.session.commit()
    
@app.cli.command()
@click.argument("id")
@click.argument("lieu")
@click.argument("date")
@click.argument("description")
def newrepetition(id,lieu,date,description):
    from .models import Repetition
    r = Repetition(id=id,lieu=lieu,date=date,description=description)
    db.session.add(r)
    db.session.commit()
