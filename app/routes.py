from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, ProjectCreation, ClientCreation
from app.models import User, FicheSuivi, Client, Societe, Projet
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title='Avant-login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash('Login successful for user {}'.format(form.username.data))
        return redirect(url_for('Accueil'))
    return render_template('login.html', title='Sign In', form=form)

#Accueil
@app.route('/Accueil')
def Accueil():
    return render_template('Accueil.html', title='Accueil')

@app.route('/FichesSuivi')
def List_FichesSuivi():
    fiche_suivi = FicheSuivi.query.all()
    return render_template('list_prj_consultation.html', title='Fiches de suivi', fiches=fiche_suivi)

@app.route('/NouveauProjet')
def AjouterProjet():
    form = ProjectCreation() 
    form2 = ClientCreation()
    form.agent.choices = [(user.username) for user in User.query.all()]
    if form.validate_on_submit() and form2.validate_on_submit():
        new_projet = Projet(
            nom = form.nom.data,
            adresse = form.adresse.data,
            client_id = new_client.id
        )    
        new_fiche = FicheSuivi(
            FSN=form.FSN.data,
            nom=form.nom.data,
            adresse=form.adresse.data,
            agent=form.agent.data,
            client_id=new_client.id,
            projet_id=new_projet.id
        )
        new_societe = Societe(
            nom=form2.nom.data,
            type_societe=form2.type_societe.data,
            domaine=form2.domaine.data,
            tel1=form2.tel1.data,
            tel2=form2.tel2.data,
            fax=form2.fax.data,
            email=form2.email.data
        )
        new_client = Client(
            societe_id=new_societe.id
        )
        db.session.add(new_societe, new_fiche, new_client, new_projet)
        db.session.commit()
    return render_template('newproject.html', title='NouveauProjet', form=form, form2=form2)
