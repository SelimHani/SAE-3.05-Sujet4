import click
from .app import app, db
from .models import Role, Equipement,Reponses_possibles, User, Sondage
from hashlib import sha256

@app.cli.command()
def syncdb():
    db.create_all()
    r1 = Role(id=1, name="Musicien")
    r2 = Role(id=2, name="Directrice")
    r3 = Role(id=3, name="Responsable")

    e1 = Equipement(id=1, nom="Costume1")
    e2 = Equipement(id=2, nom="Piano")
    e3 = Equipement(id=3, nom="Violon")
    e4 = Equipement(id=4, nom="Flute")
    e5 = Equipement(id=5, nom="Clarinette")

    re1 = Reponses_possibles(id=1, nom= "JE PARTICIPE")
    re2 = Reponses_possibles(id=2, nom="JE NE PARTICIPE PAS")

    admin = User(mail = "admin@gmail.com", password=sha256("admin".encode()).hexdigest(), role_id=3)
    
    user1 = User(mail = "a@gmail.com", password = sha256("a".encode()).hexdigest(),nom = "Jule", prenom="Lepoulet", role_id = 1)
    user2 = User(mail = "b@gmail.com", password = sha256("b".encode()).hexdigest(),nom = "Christophe", prenom="monton", role_id = 1)
    user3 = User(mail = "c@gmail.com", password = sha256("c".encode()).hexdigest(),nom = "jone", prenom="doe", role_id = 1)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.add(re1)
    db.session.add(re2)
    db.session.add(e1)
    db.session.add(e2)
    db.session.add(e3)
    db.session.add(e4)
    db.session.add(e5)
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(admin)
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

