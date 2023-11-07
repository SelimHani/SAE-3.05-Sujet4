from .app import app, db
from flask import render_template, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField,SelectMultipleField,TextAreaField
from wtforms.validators import DataRequired
from hashlib import sha256
from .models import *


@app.route("/")
def home():
    if not current_user.is_authenticated:
        return render_template(
            "acceuil_non_connecte.html"
        )
    elif current_user.get_id_role()==1:
        return render_template(
            "acceuil_musicien.html"
        )
    return render_template(
        "acceuil.html"
    )
    
@app.route("/sondages/")
def sondages():
    sondages = get_sondages()
    return render_template(
        "sondages.html",sondages=sondages
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
    equipements = SelectMultipleField("Choisis des équipements", choices=[])

class SondageForm(FlaskForm):
    nomActivite = StringField("nomActivite")
    lieuActivite = StringField("LieuActivite")
    dateActivite = DateField()
    descriptionActivite = TextAreaField("descriptionActivite")
    equipements = SelectMultipleField("Choisis des équipements", choices=[])
    next = HiddenField()


@app.route("/create-sondage/", methods=("GET", "POST",))
def creer_sondage():
    form = SondageForm()
    equipements = get_equipements()
    l = []
    for e in equipements:
        l.append(e.nom)
    form.equipements.choices = l
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    else:
        a = Activite(nom=form.nomActivite.data, lieu=form.lieuActivite.data, date=form.dateActivite.data,description=form.descriptionActivite.data)
        s = Sondage(activite=a)
        a.sondage_id= s.id
        
        noms_e = form.equipements.data
        for nom in noms_e:
            equipement=get_equipement_by_name(nom)
            a.equipements.append(equipement)
            equipement.activites.append(a)
        
        db.session.add(a) 
        db.session.add(s)
        db.session.commit()  
        return redirect(url_for("home"))
    return render_template(
        "new_sondage.html", form=form
    )
    
@app.route("/calendrier/")
def calendrier():
    return render_template(
        "calendrier.html"
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
    equipements = get_equipements()
    l = []
    for e in equipements:
        l.append(e.nom)
    form =RepetitionForm()
    form.equipements.choices = l
    if form.is_submitted():
        r = Repetition(lieu=form.lieu.data,date=form.date.data,description=form.description.data, equipements=[])
        noms_e = form.equipements.data
        print(noms_e)
        for nom in noms_e:
            print(type(nom))
            equipement=get_equipement_by_name(nom)
            print(equipement)
            print(r)
            r.equipements.append(equipement)
            equipement.repetitions.append(r)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_repetition.html", form=form )

@app.route("/profil/<id>")
def profil(id):
    u = get_user_by_id(id)
    r = u.role_id
    role = get_role_by_id(r)
    return render_template(
        "profil.html", user= u, role=role
    )    

class ChangeProfilForm(FlaskForm):
    nom = StringField("Nom")
    prenom = StringField("Prenom")
    date_nais = DateField("Date_de_naissance")
    num = StringField("Numero")
    password = PasswordField("Password")
    next = HiddenField()

class RepondreSondageForm(FlaskForm):
    reponse = SelectField('Participer?', choices=[("oui","Oui"),("non","Non")])

@app.route("/change-profil/<id>",methods=("GET","POST",))
def changer_profil(id):
    u  = get_user_by_id(id)
    f = ChangeProfilForm()
    
    if f.is_submitted():
        password_hash = sha256(f.password.data.encode()).hexdigest()
        u.nom = f.nom.data
        u.prenom = f.prenom.data
        u.num =  f.num.data
        u.password = password_hash
        db.session.commit()
        return redirect(url_for("profil",id = id))
    return render_template("changer_profil.html", form=f,user=u )

@app.route("/repondre-sondage/<id>",methods=("GET","POST",))
def repondre_sondage(id):
    s  = get_sondage_by_id(id)
    f = RepondreSondageForm()
    if f.is_submitted():
        reponse = f.reponse.data
        if  a_deja_repondu(current_user.get_id(),s.get_id()):
            r = Reponse_sondage.query.filter_by(user_id=current_user.get_id(), sondage_id=s.get_id()).first()
            r.reponse = reponse
        else:
            r = Reponse_sondage(user_id=current_user.get_id(), sondage_id=s.get_id(), user=current_user, sondage=s, reponse=reponse)
            db.session.add(r)
        
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("repondre_sondage.html", form=f,sondage=s )
