import click
from .app import app, db
from .models import *
from hashlib import sha256
from datetime import datetime

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

    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(r4)

    e1 = Accessoire(id=1, nom="Chapeau vert")
    e2 = Accessoire(id=2, nom="Lunette de piscine")
    e3 = Accessoire(id=3, nom="Cape")
    e4 = Accessoire(id=4, nom="Chapeau rouge")
    e5 = Accessoire(id=5, nom="Bonnet de bain")
    e6 = Accessoire(id=6, nom="Masque")

    i1 = Instrument(id=1, name="Flûte à bec")
    i2 = Instrument(id=2, name="Flûte traversière")
    i3 = Instrument(id=3, name="Clarinette")
    i4 = Instrument(id=4, name="Hautbois")
    i5 = Instrument(id=5, name="Saxophone")
    i6 = Instrument(id=6, name="Trompette")
    i7 = Instrument(id=7, name="Trombone")
    i8 = Instrument(id=8, name="Tuba")
    i9 = Instrument(id=9, name="Caisse claire")

    re1 = Reponses_possibles(id=1, nom="JE PARTICIPE")
    re2 = Reponses_possibles(id=2, nom="JE NE PARTICIPE PAS")
    re3 = Reponses_possibles(id=3, nom="OUI")
    re4 = Reponses_possibles(id=4, nom="NON")
    re5 = Reponses_possibles(id=5, nom="PEUT ETRE")
    re6 = Reponses_possibles(id=6, nom="VENTS")
    re7 = Reponses_possibles(id=7, nom="CUIVRES")
    re8 = Reponses_possibles(id=8, nom="PERSCUSSIONS")

    admin = User(mail="admin@gmail.com",
                 password=sha256("admin".encode()).hexdigest(),
                 num_tel="0871661865",
                 role_id=3,
                 nom="admin",
                 prenom="admin")

    user1 = User(mail="a@gmail.com",
                 password=sha256("a".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Poulet",
                 prenom="Jule",
                 role_id=1,
                 ddn=datetime.strptime("1990-01-01", "%Y-%m-%d"),
                 instrument_id=1)
    user2 = User(mail="b@gmail.com",
                 password=sha256("b".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Monton",
                 prenom="Christophe",
                 role_id=1,
                 ddn=datetime.strptime("1990-05-15", "%Y-%m-%d"),
                 instrument_id=2)
    user3 = User(mail="c@gmail.com",
                 password=sha256("c".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Doe",
                 prenom="John",
                 role_id=1,
                 ddn=datetime.strptime("1985-10-20", "%Y-%m-%d"),
                 instrument_id=3)
    user4 = User(mail="d@gmail.com",
                 password=sha256("d".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Joie",
                 prenom="Marie",
                 role_id=1,
                 ddn=datetime.strptime("1992-03-08", "%Y-%m-%d"),
                 instrument_id=4)
    user5 = User(mail="e@gmail.com",
                 password=sha256("e".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Laguitare",
                 prenom="Joe",
                 role_id=1,
                 ddn=datetime.strptime("1994-07-12", "%Y-%m-%d"),
                 instrument_id=5)
    user6 = User(mail="f@gmail.com",
                 password=sha256("f".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Tou",
                 prenom="Emma",
                 role_id=1,
                 ddn=datetime.strptime("1998-12-30", "%Y-%m-%d"),
                 instrument_id=6)
    user7 = User(mail="g@gmail.com",
                 password=sha256("g".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Macron",
                 prenom="Emmanuel",
                 role_id=1,
                 ddn=datetime.strptime("1977-12-21", "%Y-%m-%d"),
                 instrument_id=7)

    user8 = User(mail="aaa@gmail.com",
                 password=sha256("aaa".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Proche",
                 prenom="Monsieur",
                 role_id=4,
                 ddn=datetime.strptime("1977-12-21", "%Y-%m-%d"))
    user9 = User(mail="bbb@gmail.com",
                 password=sha256("bbb".encode()).hexdigest(),
                 num_tel="0871661865",
                 nom="Sy",
                 prenom="Omar",
                 role_id=4,
                 ddn=datetime.strptime("1977-12-21", "%Y-%m-%d"))

    proche1 = Proche(id=1,
                     musicien_mail="a@gmail.com",
                     proche_mail="aaa@gmail.com")
    proche2 = Proche(id=2,
                     musicien_mail="a@gmail.com",
                     proche_mail="bbb@gmail.com")
    proche3 = Proche(id=3,
                     musicien_mail="c@gmail.com",
                     proche_mail="aaa@gmail.com")

    union_musicalles = "Place de l'Église, 45150 Férolles"

    iuto = "16 Rue Issoudun, 45100 Orléans"
    r1 = Repetition(id=1,
                    lieu=union_musicalles,
                    date=datetime.strptime("2024-03-10 16:00",
                                           "%Y-%m-%d %H:%M"),
                    accessoires=[e1, e2],
                    description="repetition des percussions")
    r2 = Repetition(id=2,
                    lieu=union_musicalles,
                    date=datetime.strptime("2024-02-25 16:00",
                                           "%Y-%m-%d %H:%M"),
                    accessoires=[e1, e2, e4],
                    description="repetition des instruments à vents")
    r3 = Repetition(id=3,
                    lieu=union_musicalles,
                    date=datetime.strptime("2024-03-05 16:00",
                                           "%Y-%m-%d %H:%M"),
                    accessoires=[e3, e5],
                    description="repetition des violons et clarinette")
    r4 = Repetition(id=4,
                    lieu=union_musicalles,
                    date=datetime.strptime("2024-02-28 16:00",
                                           "%Y-%m-%d %H:%M"),
                    accessoires=[e1, e6],
                    description="repetition orchestre")
    r5 = Repetition(id=5,
                    lieu=union_musicalles,
                    date=datetime.strptime("2024-02-10 16:00",
                                           "%Y-%m-%d %H:%M"),
                    accessoires=[e1, e2, e3, e4, e5],
                    description="repetition avant le concert de noel")

    a1 = Activite(id=1,
                  nom="Concert de fevrier",
                  lieu=union_musicalles,
                  date=datetime.strptime("28/02/2024 16:00", "%d/%m/%Y %H:%M"),
                  accessoires=[e1, e2, e3, e4, e5, e6],
                  description="concert de noel avec tout l'orchestre")
    a2 = Activite(id=2,
                  nom="Orchestre",
                  lieu=iuto,
                  date=datetime.strptime("12/03/2024 16:00", "%d/%m/%Y %H:%M"),
                  accessoires=[e1, e2, e3, e4, e5, e6],
                  description="orchestre pour film à Hollywood")
    a3 = Activite(id=3,
                  nom="Concert du nouvel an",
                  lieu=iuto,
                  date=datetime.strptime("01/01/2024 16:00", "%d/%m/%Y %H:%M"),
                  accessoires=[e6],
                  description="concert de tambour, batterie, triangle")
    a4 = Activite(id=4,
                  nom="Carnaval",
                  lieu=iuto,
                  date=datetime.strptime("20/01/2024 16:00", "%d/%m/%Y %H:%M"),
                  accessoires=[e1, e2, e3, e4],
                  description="défilé carnaval depart salle des fêtes")

    s1 = Sondage(id=1,
                 activite=a1,
                 reponses_possibles=[re1, re2],
                 date_fin=datetime.strptime("2024-02-24 16:00",
                                            "%Y-%m-%d %H:%M"))
    s2 = Sondage(id=2,
                 activite=a2,
                 reponses_possibles=[re1, re2],
                 date_fin=datetime.strptime("2024-03-08 16:00",
                                            "%Y-%m-%d %H:%M"))
    s3 = Sondage(id=3,
                 activite=a3,
                 reponses_possibles=[re1, re2],
                 date_fin=datetime.strptime("2023-12-20 16:00",
                                            "%Y-%m-%d %H:%M"))
    s4 = Sondage(id=4,
                 activite=a4,
                 reponses_possibles=[re1, re2],
                 date_fin=datetime.strptime("2024-01-10 16:00",
                                            "%Y-%m-%d %H:%M"))

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)
    db.session.add(user9)
    db.session.add(i1)
    db.session.add(i2)
    db.session.add(i3)
    db.session.add(i4)
    db.session.add(i5)
    db.session.add(i6)
    db.session.add(i7)
    db.session.add(i8)
    db.session.add(i9)
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
    db.session.add(re1)
    db.session.add(re2)
    db.session.add(re3)
    db.session.add(re4)
    db.session.add(re5)
    db.session.add(re6)
    db.session.add(re7)
    db.session.add(re8)
    db.session.add(e1)
    db.session.add(e2)
    db.session.add(e3)
    db.session.add(e4)
    db.session.add(e5)
    db.session.add(e6)
    db.session.add(admin)
    db.session.add(proche1)
    db.session.add(proche2)
    db.session.add(proche3)
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

@app.cli.command()
def dropdb():
    db.drop_all()
    db.session.commit()
