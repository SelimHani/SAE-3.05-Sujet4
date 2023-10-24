from .app import app, db
from flask import render_template, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField
from wtforms.validators import DataRequired
from hashlib import sha256
from .models import User, Role, get_role_by_id

@app.route("/")
def home():
    return render_template("home.html")
    
class LoginForm(FlaskForm):
    mail = StringField("Email")
    password = PasswordField("Password")
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.mail.data)
        if user is None:
            return None
        m=sha256()
        m.update(self.password.data.encode())
        passwd= m.hexdigest()
        return user if passwd == user.password else None

class RegisterForm(FlaskForm):

    nom = StringField("Nom")
    prenom = StringField("Prenom")
    date_nais = DateField("Date_de_naissance")
    mail = EmailField("Mail")
    num = StringField("Numero")
    password = PasswordField("Password")
    role = SelectField('Role', choices=[('1', 'musicien'), ('2', 'directrice'),('3','responsable')])
    next = HiddenField()
    
    


@app.route("/login/", methods=("GET","POST",))
def login():
    f =LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("login.html",form=f)
    
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register/", methods=("GET","POST",))
def creer():
    form =RegisterForm()
    if form.is_submitted():
        password_hash = sha256(form.password.data.encode()).hexdigest()
        role_id = int(form.role.data)
        r = get_role_by_id(role_id)
        new_personne = User(mail=form.mail.data, password = password_hash , role_id = role_id, nom = form.nom.data, prenom = form.prenom.data, ddn=form.date_nais.data, num_tel = form.num.data )

        db.session.add(new_personne)
        db.session.commit()
        
        login_user(new_personne)

        return redirect(url_for("home"))

    return render_template("register.html", form=form )
