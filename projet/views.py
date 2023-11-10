
import tkinter
import sqlalchemy
from .app import app, db
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField,SelectMultipleField,TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, Regexp
from hashlib import sha256
from .models import *
from sqlalchemy import text, func


@app.route("/")
def home():

    sondages = get_sondages()

    if not current_user.is_authenticated:
        return render_template(
            "acceuil_non_connecte.html"
        )
    elif current_user.get_id_role()==1:
        return render_template(
            "acceuil_musicien.html",sondages= sondages
        )
    return render_template(
        "acceuil.html",sondages= sondages
    )
    
@app.route("/sondages/")
def sondages():
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    
    sondages= get_sondages()
        
    return render_template(
        "sondages.html",sondages=sondages
    )
class LoginForm(FlaskForm):
    mail = StringField("Email",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
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
    nom = StringField("Nom", validators=[InputRequired()])
    prenom = StringField("Prenom", validators=[InputRequired()])
    date_nais = DateField("Date_de_naissance", validators=[InputRequired()])
    mail = EmailField("Mail", validators=[InputRequired()])
    num = StringField("Numéro", validators=[InputRequired(),Regexp('^[0-9]{10}$', message="Le numéro doit contenir uniquement des chiffres."),Length(min=10, max=10, message="Le numéro doit contenir 10 chiffres.")])    
    password = PasswordField("Password", validators=[InputRequired()])

    role = SelectField('Role', choices=[("1","Musicien"),("2","Directrice"),("3","Responsable")])
    next = HiddenField()

class RepetitionForm(FlaskForm):
    id = HiddenField("Id")
    lieu = StringField("Lieu",validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    description = StringField("Description")
    equipements = SelectMultipleField("Choisis des équipements", choices=[])


class SondageParticipationForm(FlaskForm):
    nomActivite = StringField("nomActivite")
    lieuActivite = StringField("LieuActivite")
    dateActivite = DateField()

class SondageForm(FlaskForm):
    nomActivite = StringField("nomActivite",validators=[InputRequired()])
    lieuActivite = StringField("LieuActivite",validators=[InputRequired()])
    dateActivite = DateField(validators=[InputRequired()])
    descriptionActivite = TextAreaField("descriptionActivite")
    equipements = SelectMultipleField("Choisis des équipements", choices=[])
    next = HiddenField()
    
class SondageSatisfactionForm(FlaskForm):
    question =  StringField("Question",validators=[InputRequired()])
    reponses = StringField("Reponses_possibles",validators=[InputRequired()])
    next = HiddenField()



@app.route("/create-sondage-participation/", methods=("GET", "POST",))
def creer_sondage_participation():
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home")) 
    except AttributeError:
        return redirect(url_for("home"))
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
        r1 = get_reponses_possibles_by_id(1)
        r2 = get_reponses_possibles_by_id(2)
        s.reponses_possibles.append(r1)
        s.reponses_possibles.append(r2)
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
    
@app.route("/create-sondage-satisfaction/", methods=("GET", "POST",))
def creer_sondage_satisfaction():
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home")) 
    except AttributeError:
        return redirect(url_for("home"))
    form = SondageSatisfactionForm()
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    else:
        question = form.question.data
        reponse = form.reponses.data
        r = Reponses_possibles(nom=reponse)
        db.session.add(r)
        if get_sondage_by_question(question) == None:   
            s = Sondage(question = form.question.data)
            s.reponses_possibles.append(r)
            db.session.add(s)
            db.session.commit()
        else:
            s = get_sondage_by_question(question)
            s.reponses_possibles.append(r)
            db.session.commit()   
        form.reponses.data=""
    return render_template("new_sondage_satisfaction.html",form=form)
    
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

import tkinter
from tkinter import messagebox

def afficher_popup(message):
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo("Message", message)
    root.destroy()




@app.route("/create-user/", methods=("GET","POST",))
def creer_user():
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home")) 
    except AttributeError:
        return redirect(url_for("home"))
    form =RegisterForm()
    if form.is_submitted():
        try:
            password_hash = sha256(form.password.data.encode()).hexdigest()
            role_id = int(form.role.data)
            new_personne = User(mail=form.mail.data,password=password_hash,role_id=role_id,nom=form.nom.data,prenom=form.prenom.data,ddn=form.date_nais.data,num_tel=form.num.data)

            db.session.add(new_personne)
            db.session.commit()

            flash('Utilisateur créé avec succès!', 'success')
            return redirect(url_for("home"))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            afficher_popup('Ce mail est déjà utilisé,veuillez utiliser un autre.')

        except sqlalchemy.exc.PendingRollbackError:
            db.session.rollback()
            afficher_popup('Ce mail est déjà utilisé, veuillez utiliser un autre .')
            


    return render_template("register.html", form=form)

@app.route("/calendrier/")
def calendrier():
    return render_template("calendrier.html")

@app.route("/repetitions")
def repetitions():
    repetitions_activites = get_calendrier()
    return render_template("repetitions.html", repetitions_activites=repetitions_activites)

@app.route("/create-repetition/", methods=("GET","POST",))
def creer_repetition():
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home")) 
    except AttributeError:
        return redirect(url_for("home"))
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
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    u = get_user_by_id(id)
    r = u.role_id
    role = get_role_by_id(r)
    participees = u.repetitions
    nb_participees = len(participees)
    now = func.now()
    passees = Repetition.query.filter(Repetition.date <= now).all()
    ratees = len(passees)-nb_participees
    
    return render_template(
        "statistique.html", user= u, role=role, nb_participees=nb_participees, ratees=ratees
    )    

class ChangeProfilForm(FlaskForm):
    nom = StringField("Nom")
    prenom = StringField("Prenom")
    date_nais = DateField("Date_de_naissance")
    num = StringField("Numero")
    password = PasswordField("Password")
    next = HiddenField()

class RepondreSondageForm(FlaskForm):
    reponse = SelectField('Participer?', choices=[])

@app.route("/change-profil/<id>",methods=("GET","POST",))
def changer_profil(id):
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    u  = get_user_by_id(id)
    f = ChangeProfilForm()
    
    if f.is_submitted():
        if f.password.data !="":
            password_hash = sha256(f.password.data.encode()).hexdigest()
            u.password = password_hash
        u.nom = f.nom.data
        u.prenom = f.prenom.data
        u.num =  f.num.data
        
        db.session.commit()
        return redirect(url_for("profil",id = id))
    return render_template("changer_profil.html", form=f,user=u )

@app.route("/repondre-sondage/<id>",methods=("GET","POST",))
def repondre_sondage(id):
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    s  = get_sondage_by_id(id)
    reponses = get_reponses_possibles_by_sondage(s)
    l=[]
    print(reponses)
    for r in reponses:
        l.append((r.id,r.nom))
    print(l)
    f = RepondreSondageForm()
    f.reponse.choices= l
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
    
    
    lieu = s.activite.lieu
    lieuM =''
    for c in lieu:
        if (c == ' '):
            lieuM += '+'
        else:
            lieuM += c
    map = "https://www.google.fr/maps/search/"+lieuM+"/"
    return render_template("repondre_sondage.html", form=f,sondage=s, lieu_map = map)


@app.route("/type-sondage/")
def type_sondage():
    return render_template("choix_type_sondage.html")

class EquipementForm(FlaskForm):
    nom = StringField("nom")
    
    
@app.route("/ajoute-equipement",methods=("GET","POST",))
def ajoute_equipement():
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home")) 
    except AttributeError:
        return redirect(url_for("home"))
    form =EquipementForm()
    if form.is_submitted():
        e = Equipement(nom=form.nom.data)
        db.session.add(e)
        db.session.commit()
        form.nom.data  = ""
    return render_template("ajoute_equipement.html", form=form )







@app.route("/delete-sondage/<id>")
def delete_sondage(id):
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home")) 
    except AttributeError:
        return redirect(url_for("home"))
    s = Sondage.query.get(id)
    reponses = Reponse_sondage.query.filter_by(sondage_id=id).all()
    a = s.activite
    equipements = a.equipements
    for e in equipements:
        sql_query=text('DELETE FROM exiger WHERE activite_id = :activite_id AND equipement_id = :equipement_id')
        db.session.execute(sql_query,{"activite_id":a.id,"equipement_id":e.id})
    db.session.commit()
    db.session.delete(a)
    for r in reponses:
        db.session.delete(r)
    db.session.commit()
    db.session.delete(s)
    db.session.commit()
    print("aaaaaaaaaaaaaaa")
    return redirect(url_for("sondages"))

@app.route("/detail-repetition/<id>")
def detail_repetition(id):
    r = get_repetition_by_id(id)
    return render_template("detail_repetition.html",r=r)


@app.route("/feuille-presence/")
def feuille_presence():
    r = Repetition.query.all()
    return render_template("feuille_presence.html", r =r)

class PresenceForm(FlaskForm):
    musicien = SelectMultipleField("Choisis des musiciens", choices=[])
    
@app.route("/presence-repetition/<id>",methods=("GET","POST",))
def presence_repetition(id):
    r = get_repetition_by_id(id)
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    musiciens = User.query.filter_by(role_id=1).all()
    form = PresenceForm()
    l=[]
    
   
    for m in musiciens:
        l.append((m.mail, m.nom))
    form.musicien.choices=l
    
    if form.is_submitted():
        print("aaaaaaa")
        reponse = form.musicien.data
        for mail in reponse:
            u = User.query.get(mail)
            r.users.append(u)
            u.repetitions.append(r)
        db.session.commit()
        print("aaaaaaaaaaaaaa")
        return redirect(url_for("home"))
    return render_template("presence_repetition.html", form=form,id= r.id)


@app.route("/reponse_sond.html/<id>")
def reponse_sondage(id):
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home")) 
    except AttributeError:
        return redirect(url_for("home"))
    l = []
    s = Sondage.query.get(id)
    reponses = Reponse_sondage.query.filter_by(sondage_id=id).all()
    for elem in reponses:
        l.append((Reponses_possibles.query.get(elem.reponse).nom,User.query.get(elem.user_id).nom,User.query.get(elem.user_id).prenom))
    return render_template("reponse_sond.html", l=l)
