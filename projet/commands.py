import click
from .app import app, db

@app.cli.command()

def syncdb():
    db.create_all()
    
@app.cli.command()
@click.argument("username")
@click.argument("password")
@click.argument("role")

def newuser(username, password, role):
    from .models import User
    from hashlib import sha256
    m=sha256()
    m.update(password.encode())
    u=User(username=username, password=m.hexdigest(), role=role)
    db.session.add(u)
    db.session.commit()