from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, ProjectCreation, ClientCreation, AgentCreation
from app.models import User, FicheSuivi, Client, Societe, Projet, Personne
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash

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

@app.route('/NouveauProjet', methods=['GET', 'POST'])
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
            fsn = new_fiche.generate_fsn(),
            projet=form.nom.data,
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

@app.route('/CreerAgent', methods=['GET', 'POST'])
def CreerAgent():
    form = AgentCreation()
    if current_user.privilege == 'admin':
        if form.validate_on_submit():
            new_agent = Personne(
                nom=form.nom.data,
                prenom=form.prenom.data,
                adresse=form.adresse.data,
                tel=form.tel.data,
                gsm=form.gsm.data,
                email=form.email.data
            )
            password_hash = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                password=password_hash,
                privilege=form.privilege.data,
                personne_id=new_agent.id
            )
            db.session.add(new_agent, new_user)
            db.session.commit()
    return render_template('creer_agent.html', title='NouveauAgent', form=form)

@app.route('/projet/<int:projet_id>')
def AfficherProjet(projet_id):
    projet = FicheSuivi.query.get_or_404(projet_id)
    return render_template('projet.html', title='Projet', projet=projet)