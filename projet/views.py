from .app import app, db
from flask import render_template, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField,SelectMultipleField,TextAreaField
from wtforms.validators import DataRequired
from hashlib import sha256
from .models import User, get_role_by_id, get_repetitions, Repetition


@app.route("/")
def home():
    return render_template(
        "acceuil_non_connecte.html"
    )
class LoginForm(FlaskForm):
    mail = StringField("Email")
    password = PasswordField("Password")
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.mail.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class RegisterForm(FlaskForm):    
    nom = StringField("Nom")
    prenom = StringField("Prenom")
    date_nais = DateField("Date_de_naissance")
    mail = EmailField("Mail")
    num = StringField("Numero")
    password = PasswordField("Password")
    role = SelectField('Role', choices=[("1","Musicien"),("2","Directrice"),("3","Responsable")])
    next = HiddenField()
    
class RepetitionForm(FlaskForm):
    id = HiddenField("Id")
    lieu = StringField("Lieu")
    date = DateField("Date")
    description = StringField("Description")

class SondageForm(FlaskForm):
    nomActivite = StringField("nomActivite")
    lieuActivite = StringField("LieuActivite")
    dateActivite = DateField()
    descriptionActivite = TextAreaField("descriptionActivite")
    next = HiddenField()


@app.route("/create-sondage/", methods=("GET", "POST",))
def creer_sondage():
    f = SondageForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    return render_template(
        "new_sondage.html", form=f
    )


@app.route("/login/", methods=("GET", "POST",))
def login():
    f = LoginForm()
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


@app.route("/create-user/", methods=("GET","POST",))
def creer_user():
    form =RegisterForm()
    if form.is_submitted():
        password_hash = sha256(form.password.data.encode()).hexdigest()
        role_id = int(form.role.data)
        new_personne = User(mail=form.mail.data, password = password_hash , role_id = role_id, nom = form.nom.data, prenom = form.prenom.data, ddn=form.date_nais.data, num_tel = form.num.data )

        db.session.add(new_personne)
        db.session.commit()
        
        login_user(new_personne)

        return redirect(url_for("home"))

    return render_template("register.html", form=form )

@app.route("/repetitions/")
def repetitions():
    repetitions = get_repetitions()
    return render_template("repetitions.html", repetitions=repetitions)


@app.route("/create-repetition/", methods=("GET","POST",))
def creer_repetition():
    form =RepetitionForm()
    if form.is_submitted():
        r = Repetition(lieu=form.lieu.data,date=form.date.data,description=form.description.data)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_repetition.html", form=form )