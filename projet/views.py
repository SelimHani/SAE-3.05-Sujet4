import tkinter
import sqlalchemy
import unidecode
from .app import app, db
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField,SelectMultipleField,TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, Regexp
from hashlib import sha256
from .models import *
from sqlalchemy import text, func
from flask import jsonify
from tkinter import messagebox


def est_present(adresse):
    """Vérifie si un proche est associé au musicien

    Args:
        adresse (string): adresse mail du musicien

    Returns:
        boolean
    """
    proche_entry = Proche.query.filter_by(proche_mail=adresse).first()
    return proche_entry.musicien_mail if proche_entry else False

@app.route("/")
def home():
    """Affiche la page d'accueil
    """
    sondages = get_sondages()
    repetitions_activites = get_calendrier()
    derniere_repetition = None
    
    try:
        derniere_repetition = repetitions_activites[0:5]
    except IndexError:
        derniere_repetition = None
    if not current_user.is_authenticated:
        return render_template("accueil_non_connecte.html")
    elif current_user.get_id_role() == 1:
        return render_template("accueil_musicien.html",
                               sondages=sondages,
                               prochain_evenement=derniere_repetition,
                               user=current_user)

    return render_template("accueil.html",
                           sondages=sondages,
                           prochain_evenement=derniere_repetition,
                           user=current_user)

@app.route("/sondages/")
def sondages():
    """Affiche la page des sondages en cours
    """
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    sondages= get_sondages()

    return render_template(
        "sondages.html",sondages=sondages,user=current_user
    )

@app.route("/sondages-finis/")
def sondages_finis():
    """Affiche la page des sondages finis
    """
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    sondages_finis= get_sondages_finis()

    return render_template(
        "sondages_finis.html",sondages=sondages_finis,user=current_user
    )


class LoginForm(FlaskForm):
    mail = StringField("Email",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        """Renvoie l'utilisateur connecté
        """
        user = User.query.get(self.mail.data)
        if user is None:
            return None
        if user.role_id == 4:
            musicien = est_present(self.mail.data)
            if musicien:
                musicien_user = User.query.get(musicien)
                if musicien_user:
                    m = sha256()
                    m.update(self.password.data.encode())
                    passwd = m.hexdigest()
                    return musicien_user if passwd == user.password else None
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()

        # Comparaison du hash des mots de passe
        return user if passwd == user.password else None

class ProcheForm(FlaskForm):
    nom = StringField("Nom", validators=[InputRequired()])
    prenom = StringField("Prenom", validators=[InputRequired()])
    mail = EmailField("Mail", validators=[InputRequired()])
    date_nais = DateField("Date_de_naissance", validators=[InputRequired()])
    num = StringField("Numéro", validators=[InputRequired(),Regexp('^[0-9]{10}$', message="Le numéro doit contenir uniquement des chiffres."),Length(min=10, max=10, message="Le numéro doit contenir 10 chiffres.")])
    password = PasswordField("Password", validators=[InputRequired()])
    musicien = SelectField('Musicien')
    next = HiddenField()

@app.route("/create-proche/", methods=("GET", "POST",))
def creer_proche():
    """Affiche le formulaire de création d'un proche
    """
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    form =ProcheForm()
    form.musicien.choices = [(user.mail, f"{user.nom} {user.prenom}") for user in User.query.filter_by(role_id=1).all()]

    if form.is_submitted():
        try:
            password_hash = sha256(form.password.data.encode()).hexdigest()
            role_id = 4
            new_personne = User(mail=form.mail.data,password=password_hash,role_id=role_id,nom=form.nom.data,prenom=form.prenom.data,ddn=form.date_nais.data,num_tel=form.num.data)

            proche = Proche(proche_mail=form.mail.data, musicien_mail=form.musicien.data)

            db.session.add(proche)
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
    return render_template("create-proche.html", form=form,user=current_user)





class RegisterForm(FlaskForm):
    nom = StringField("Nom", validators=[InputRequired()])
    prenom = StringField("Prenom", validators=[InputRequired()])
    date_nais = DateField("Date_de_naissance", validators=[InputRequired()])
    mail = EmailField("Mail", validators=[InputRequired()])
    num = StringField("Numéro", validators=[InputRequired(),Regexp('^[0-9]{10}$', message="Le numéro doit contenir uniquement des chiffres."),Length(min=10, max=10, message="Le numéro doit contenir 10 chiffres.")])
    password = PasswordField("Password", validators=[InputRequired()])
    role = SelectField('Role', choices=[("1","Musicien"),("2","Directrice"),("3","Responsable")])
    instrument = SelectField('Role', choices=[])
    next = HiddenField()

class RepetitionForm(FlaskForm):
    id = HiddenField("Id")
    lieu = StringField("Lieu",validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    description = StringField("Description")
    accessoires = SelectMultipleField("Choisis des équipements", choices=[])


class SondageForm(FlaskForm):
    nomActivite = StringField("nomActivite",validators=[InputRequired()])
    lieuActivite = StringField("LieuActivite",validators=[InputRequired()])
    dateActivite = DateField(validators=[InputRequired()])
    descriptionActivite = TextAreaField("descriptionActivite")
    accessoires = SelectMultipleField("Choisis des équipements", choices=[])
    dateFin = DateField(validators=[InputRequired()])
    next = HiddenField()

class SondageSatisfactionForm(FlaskForm):
    question =  StringField("Question",validators=[InputRequired()])
    reponses = StringField("Reponses_possibles",validators=[InputRequired()])
    dateFin = DateField(validators=[InputRequired()])
    next = HiddenField()



@app.route("/create-sondage-participation/", methods=("GET", "POST",))
def creer_sondage_participation():
    """Affiche le formulaire de création d'un sondage de participation
    """
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    form = SondageForm()
    accessoires = get_accessoires()
    l = []
    for e in accessoires:
        l.append(e.nom)
    form.accessoires.choices = l
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    else:
        a = Activite(nom=form.nomActivite.data, lieu=form.lieuActivite.data, date=form.dateActivite.data,description=form.descriptionActivite.data)
        s = Sondage(activite=a,date_fin = form.dateFin.data)
        a.sondage_id= s.id
        r1 = get_reponses_possibles_by_id(1)
        r2 = get_reponses_possibles_by_id(2)
        s.reponses_possibles.append(r1)
        s.reponses_possibles.append(r2)
        noms_e = form.accessoires.data
        for nom in noms_e:
            accessoire=get_accessoire_by_name(nom)
            a.accessoires.append(accessoire)
            accessoire.activites.append(a)

        db.session.add(a)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template(
        "new_sondage.html", form=form,user=current_user
    )

@app.route("/create-sondage-satisfaction/", methods=("GET", "POST",))
def creer_sondage_satisfaction():
    """Affiche le formulaire de création d'un sondage de satisfaction
    """
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
            s = Sondage(question = form.question.data,date_fin = form.dateFin.data)
            s.reponses_possibles.append(r)
            db.session.add(s)
            db.session.commit()
        else:
            s = get_sondage_by_question(question)
            s.reponses_possibles.append(r)
            db.session.commit()
        form.reponses.data=""
    return render_template("new_sondage_satisfaction.html",form=form,user=current_user)

@app.route("/login/", methods=("GET", "POST",))
def login():
    """Affiche la page de login
    """
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("login.html",form=f,user=current_user)

@app.route("/logout/")
def logout():
    """Pour se déconnecter
    """
    logout_user()
    return redirect(url_for("home"))


def afficher_popup(message):
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo("Message", message)
    root.destroy()




@app.route("/create-user/", methods=("GET","POST",))
def creer_user():
    """Affiche le formulaire de création d'un utilisateur
    """
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    form =RegisterForm()
    instruments = get_instruments()
    l = []
    for i in instruments:
        l.append((i.id,i.name))
    form.instrument.choices = l
    if form.is_submitted():
        try:
            password_hash = sha256(form.password.data.encode()).hexdigest()
            role_id = int(form.role.data)
            instrument_id = int(form.instrument.data)
            new_personne = User(mail=form.mail.data,password=password_hash,role_id=role_id,nom=form.nom.data,prenom=form.prenom.data,ddn=form.date_nais.data,num_tel=form.num.data, instrument_id=instrument_id)

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



    return render_template("register.html", form=form,user=current_user)



@app.route("/create-repetition/", methods=("GET","POST",))
def creer_repetition():
    """Affiche le formulaire de création de répétition
    """
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    accessoires = get_accessoires()
    l = []
    for e in accessoires:
        l.append(e.nom)
    form =RepetitionForm()
    form.accessoires.choices = l
    if form.is_submitted():
        r = Repetition(lieu=form.lieu.data,date=form.date.data,description=form.description.data, accessoires=[])
        noms_e = form.accessoires.data
        print(noms_e)
        for nom in noms_e:
            print(type(nom))
            accessoire=get_accessoire_by_name(nom)
            print(accessoire)
            print(r)
            r.accessoires.append(accessoire)
            accessoire.repetitions.append(r)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_repetition.html", form=form,user=current_user )

@app.route("/profil/<id>")
def profil(id):
    """Affiche la page de profil d'un utilisateur
    """
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
    if passees == []:
        return render_template("statistique.html", user= u, role=role, nb_participees=nb_participees, ratees=ratees,pourcentage=0)

    pourcentage = int((nb_participees/len(passees))*100)

    return render_template("statistique.html", user= u, role=role, nb_participees=nb_participees, ratees=ratees,pourcentage=pourcentage)


class ChangeProfilForm(FlaskForm):
    nom = StringField("Nom")
    prenom = StringField("Prenom")
    date_nais = DateField("Date_de_naissance")
    num = StringField("Numero")
    password = PasswordField("Password")
    instrument  = SelectField("Instrument",choices = [])
    next = HiddenField()

class RepondreSondageForm(FlaskForm):
    reponse = SelectField('Participer?', choices=[])

@app.route("/change-profil/<id>",methods=("GET","POST",))
def changer_profil(id):
    """Affiche le formulaire de mise à jour de profil
    """
    try:
        if current_user.get_id_role()==1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    u  = get_user_by_id(id)
    f = ChangeProfilForm()
    
    instruments = get_instruments()
    l = []
    for i in instruments:
        l.append((i.id,i.name))
    f.instrument.choices = l

    if f.is_submitted():
        if f.password.data !="":
            password_hash = sha256(f.password.data.encode()).hexdigest()
            u.password = password_hash
        u.nom = f.nom.data
        u.prenom = f.prenom.data
        u.num =  f.num.data
        u.instrument_id = f.instrument.data

        db.session.commit()
        return redirect(url_for("profil",id = id))
    return render_template("changer_profil.html", form=f,user=u )

@app.route("/repondre-sondage/<id>",methods=("GET","POST",))
def repondre_sondage(id):
    """Affiche le formulaire pour répondre à un sondage
    """
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

    if s.question==None:
        lieu = s.activite.lieu
        lieuM =''
        for c in lieu:
            if (c == ' '):
                lieuM += '+'
            else:
                lieuM += c
        map = "https://www.google.fr/maps/search/"+lieuM+"/"
    else:
        lieuM=None
        map=None
    
    return render_template("repondre_sondage.html", form=f,sondage=s, lieu_map = map,user=current_user)


@app.route("/type-sondage/")
def type_sondage():
    """Affiche la page de selection du type de sondage pour le créer
    """
    return render_template("choix_type_sondage.html",user=current_user)

class accessoireForm(FlaskForm):
    nom = StringField("nom")


@app.route("/ajouter-accessoire",methods=("GET","POST",))
def ajoute_accessoire():
    """Affiche la page de formulaire pour créer un équipement
    """
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    form =accessoireForm()
    if form.is_submitted():
        nom_accessoire = form.nom.data
        nom_accessoire = nom_accessoire.upper() # en majuscule
        nom_accessoire = unidecode.unidecode(nom_accessoire) # suppression des accents qui restent
        accessoires = get_accessoires()

        for eq in accessoires:
            nom = eq.get_nom()
            nom = nom.upper()
            nom =unidecode.unidecode(nom)
            if nom == nom_accessoire:
                return render_template("ajouter_accessoire.html", form=form ,erreur=1,user=current_user)         
        e = Accessoire(nom=form.nom.data)
        db.session.add(e)
        db.session.commit()
        form.nom.data  = ""
        return render_template("ajouter_accessoire.html", form=form ,erreur=0,user=current_user)
    return render_template("ajouter_accessoire.html", form=form,user=current_user)


@app.route("/delete-sondage/<id>")
def delete_sondage(id):
    """Permet de supprimer un sondage
    """
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    s = Sondage.query.get(id)
    reponses = Reponse_sondage.query.filter_by(sondage_id=id).all()
    if s.activite:
        a = s.activite
        accessoires = a.accessoires
        for e in accessoires:
            sql_query=text('DELETE FROM exiger WHERE activite_id = :activite_id AND accessoire_id = :accessoire_id')
            db.session.execute(sql_query,{"activite_id":a.id,"accessoire_id":e.id})
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
    """Affiche la page de détail d"une répétition
    """
    r = get_repetition_by_id(id)
    return render_template("detail_repetition.html",r=r,user=current_user)


@app.route("/feuille-presence/")
def feuille_presence():
    """Affiche la page où choisir une répétition pour gérer les présents
    """
    r = Repetition.query.filter(Repetition.date <= func.now()).all()
    return render_template("feuille_presence.html", r =r,user=current_user)

class PresenceForm(FlaskForm):
    musicien = SelectMultipleField("Choisis des musiciens", choices=[])

@app.route("/presence-repetition/<id>",methods=("GET","POST",))
def presence_repetition(id):
    """Affiche la page pour gérer les présents lors d"une répétition
    """
    r = get_repetition_by_id(id)

    try:
        if current_user.get_id_role() == 1:
            pass
    except AttributeError:
        return redirect(url_for("home"))
    musiciens = User.query.filter_by(role_id=1).all()
    musiciens = sorted(musiciens,key=lambda item: item.nom)
    form = PresenceForm()

    l=[]

    if form.is_submitted():
        reponse = form.musicien.data
        for mail in reponse:
            u = User.query.get(mail)
            if u not in r.users:
                r.users.append(u)
                u.repetitions.append(r)
        db.session.commit()
    participent = get_musiciens_repetition(id)
    for m in musiciens:
        if m not in Repetition.query.get(id).users:
            l.append((m.mail, m.nom+" "+m.prenom))
    form.musicien.choices=l
    return render_template("presence_repetition.html", form=form,id= r.id,musiciens =participent,user=current_user)


@app.route('/retirer/<email>/<id>/', methods=['GET', 'POST'])
def retirer(email, id):
    """Permet de retirer d'une répétition un utilisateur qui a été selectionné
    """
    form = PresenceForm()

    sql_query=text('DELETE FROM participer WHERE user_id = :user_id AND repetition_id = :repetition_id')
    db.session.execute(sql_query,{"user_id":email,"repetition_id":id})
    db.session.commit()

    l=[]
    non_participants = get_musiciens_pas_repetition(id)
    for m in non_participants:
        if m not in Repetition.query.get(id).users:
            l.append((m.mail, m.nom+" "+m.prenom))
    form.musicien.choices=l
    participent = get_musiciens_repetition(id)
    return render_template("presence_repetition.html", form=form,id=id,musiciens =participent,user=current_user)
 

@app.route("/reponse_sond.html/<id>")
def reponse_sondage(id):
    """Affiche la page des réponses d'un sondages
    """
    try:
        if current_user.get_id_role()==1:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    l = []
    s  = get_sondage_by_id(id)
    reponses = Reponse_sondage.query.filter_by(sondage_id=id).all()
    for elem in reponses:
        l.append((Reponses_possibles.query.get(elem.reponse).nom,User.query.get(elem.user_id).nom,User.query.get(elem.user_id).prenom))

    return render_template("reponse_sond.html", l=l, sondage = s,user=current_user)


@app.route("/gerer-presences/")
def gerer_presences():
    """Affiche une page qui permet de gérer les musiciens
    """
    return render_template("gerer_presences.html",user=current_user)


@app.route("/stats-musiciens/")
def stats_musiciens():
    """Affiche les stats des musiciens
    """
    u = User.query.filter_by(role_id=1)
    return render_template("stats_musiciens.html", users=u,user=current_user)

@app.route("/supprimer-musicien/<id>")
def supprimer_musicien(id):
    """Permet de supprimer un musicien de la base de données
    """
    user = get_user_by_id(id)
    try:
        if current_user.get_id_role()==1 or user.get_id_role()==3:
            return redirect(url_for("home"))
    except AttributeError:
        return redirect(url_for("home"))
    reponses = Reponse_sondage.query.filter_by(user_id=id).all()
    for r in reponses:
        db.session.delete(r)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update_mode', methods=['POST'])
def update_mode():
    user = current_user
    if user.mode != "sombre":
        new_mode = request.json.get('new_mode')
        user.mode = new_mode  
    else:
        user.mode = "default"
    db.session.commit()
    
    return 'Mode mis à jour avec succès', 200


@app.route('/calendrier')
def calendrier():
    events = get_calendrier_all()

    # Formattez les données pour les rendre compatibles avec FullCalendar
    events_data = []
    for event in events:
        if  event.type =="activite":
            events_data.append({
                'title': event.nom,
                'start': event.date,
                'end': event.date,
                'url': url_for("repondre_sondage", id=event.id),
            })
    else:
        events_data.append({
            'title': "Repetition",
            'start': event.date,
            'end': event.date,
            'url': url_for("detail_repetition", id=event.id),
        })

    return render_template('calendrier.html', events_data=events_data, user=current_user)
