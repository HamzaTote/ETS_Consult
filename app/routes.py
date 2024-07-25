from app import app, db
from flask import render_template, flash, redirect, url_for, current_app
from app.forms import LoginForm, ProjectCreation, SocieteCreation, UserCreation, ContactCreation, UserModification, PrestationCreation, ProjetModification
from app.models import User, FicheSuivi, Client, Societe, Personne, Prestation
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload






def admin_required(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.privilege == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('Accueil'))
    return wrapper


# login related

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Incorrect username.', 'danger')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, form.password.data):
            flash('Incorrect password.', 'danger')
            return redirect(url_for('login'))
        print("user validated")
        login_user(user)
        return redirect(url_for('Accueil'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))







#Accueil
@login_required
@app.route('/Accueil')
def Accueil():
    return render_template('Accueil.html', title='Accueil')







# project related

@login_required
@app.route('/NouveauProjet', methods=['GET', 'POST'])
def AjouterProjet():
    form = ProjectCreation()
    form2 = SocieteCreation()

    form.agent.choices = [(user.username, user.username) for user in User.query.all()]
    form.client.choices = [(client.id, client.societe.nom if client.societe and client.societe.nom else client.personne.nom) for client in Client.query.all()]

    user = User.query.filter_by(username=form.agent.data).first()
    if form.validate_on_submit():
        print("form validated")
        unique_fsn = FicheSuivi.generate_fsn()
        

        new_fiche = FicheSuivi(
            FSN=unique_fsn,
            projet=form.nom.data,
            adresse=form.adresse.data,
            user_id=user.id,
            client_id=form.client.data
        )
        
        db.session.add(new_fiche)
        db.session.commit()
        return redirect(url_for('Accueil'))
    return render_template('newproject.html', title='NouveauProjet', form=form, form2=form2)

@login_required
@app.route('/FichesSuivi')
def List_FichesSuivi():
    fiche_suivi = FicheSuivi.query.all()
    return render_template('list_prj_consultation.html', title='Fiches de suivi', fiches=fiche_suivi)

@app.route('/SupprimerProjet/<int:projet_id>', methods=['POST'])
@login_required
def SupprProjet(projet_id):
    project = FicheSuivi.query.get_or_404(projet_id)
    
    db.session.delete(project)
    db.session.commit()
    flash('Projet supprimé avec succès', 'success')
    return redirect(url_for('List_FichesSuivi'))

@login_required
@app.route('/projet/<int:id>', methods=['GET', 'POST'])
def AfficherProjet(id):
    projet = FicheSuivi.query.get_or_404(id)
    prestations = Prestation.query.filter_by(fiche_suivi_id = id).all()
    return render_template('afficher_projet.html', title='Projet', projet=projet, prestations=prestations, fiche_suivi_id=id)

@login_required
@app.route('/creer_prestation/<int:fiche_suivi_id>', methods=['GET', 'POST'])
def CreerPrestation(fiche_suivi_id):
    form = PrestationCreation()
    if form.validate_on_submit():
        new_prestation = Prestation(
            fiche_suivi_id=fiche_suivi_id,
            type_prestation=form.type.data,
            description=form.description.data,
            code = form.code.data
        )
        db.session.add(new_prestation)
        db.session.commit()
        return redirect(url_for('AfficherProjet', id=fiche_suivi_id))
    return render_template('creer_prestation.html', title='Nouvelle Prestation', form=form, fiche_suivi_id=fiche_suivi_id)

@login_required
@app.route('/modifier_projet/<int:id>', methods=['GET', 'POST'])
def ModifierProjet(id):
    projet = FicheSuivi.query.get_or_404(id)
    form = ProjetModification(obj = projet)
    form.agent.choices = [(user.username, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        if form.nom.data:
            projet.projet = form.nom.data
        if form.adresse.data:
            projet.adresse = form.adresse.data
        if form.agent.data:
            selected_user = User.query.filter_by(username=form.agent.data).first()
            if selected_user:
                projet.user_id = selected_user.id
        db.session.commit()
        return redirect(url_for('List_FichesSuivi'))
    return render_template('modifier_projet.html', title='ModifierProjet', form=form, fiche=projet)







# client related

@login_required
@app.route('/CreerClient', methods=['GET', 'POST'])
def CreerClient():
    form = ContactCreation()
    form2 = SocieteCreation()
    new_personne = None
    new_societe = None
    new_client = None
       
    if form2.validate_on_submit() and form.validate_on_submit():
        
        existing_societe = Societe.query.filter(
            (Societe.email == form2.email.data) |
            (Societe.tel1 == form2.tel1.data)
        ).first()
        existing_personne = Personne.query.filter(
            (Personne.email == form.email_contact.data) | 
            (Personne.tel == form.tel.data)
        ).first()
        
        if existing_societe:
            flash('Client déjà existant', 'danger')
        else:
            new_personne = Personne(
                nom=form.nom_contact.data,
                prenom=form.prenom.data,
                adresse=form.adresse.data,
                tel=form.tel.data,
                gsm=form.gsm.data,
                email=form.email_contact.data
            )
            db.session.add(new_personne)
            db.session.commit()

            new_societe = Societe(
                nom=form2.nom.data,
                type_societe=form2.type_societe.data,
                domaine=form2.domaine.data,
                tel1=form2.tel1.data,
                tel2=form2.tel2.data,
                fax=form2.fax.data,
                email=form2.email.data
            )
            db.session.add(new_societe)
            db.session.commit()

            new_client = Client(
                personne_id=new_personne.id,
                societe_id=new_societe.id
            )
            db.session.add(new_client)
            db.session.commit()
            
            return redirect(url_for('AjouterProjet'))
    elif form.validate_on_submit():
        existing_personne = Personne.query.filter(
            (Personne.email == form.email_contact.data) | 
            (Personne.tel == form.tel.data)
        ).first()
        if existing_personne:
            flash('Personne déjà existante', 'danger')
        else:
            new_personne = Personne(
                nom=form.nom_contact.data,
                prenom=form.prenom.data,
                adresse=form.adresse.data,
                tel=form.tel.data,
                gsm=form.gsm.data,
                email=form.email_contact.data
            )
            db.session.add(new_personne)
            db.session.commit()

            new_client = Client(
                personne_id=new_personne.id
            )
            db.session.add(new_client)
            db.session.commit()
            
            return redirect(url_for('AjouterProjet'))    
    else:
        print("Form Errors: ", form.errors)
        print("Form2 Errors: ", form2.errors)

    return render_template('nouveau_client.html', title='NouveauClient', form=form, form2=form2)

@login_required
@app.route('/liste_clients')
def ListClients():
    clients = Client.query.options(joinedload(Client.personne), joinedload(Client.societe)).all()
    return render_template('list_clients.html', title='Clients', clients=clients)

@login_required
@app.route('/modifier_client/<int:id>', methods=['GET', 'POST'])
def ModifierClient(id):
    client = Client.query.get_or_404(id)
    form = ContactCreation(obj = client.personne)
    form2 = SocieteCreation(obj = client.societe)
    if form.validate_on_submit() and form2.validate_on_submit():
        if form.nom_contact.data:
            client.personne.nom = form.nom_contact.data
        if form.prenom.data:
            client.personne.prenom = form.prenom.data
        if form.adresse.data:
            client.personne.adresse = form.adresse.data
        if form.tel.data:
            client.personne.tel = form.tel.data
        if form.gsm.data:
            client.personne.gsm = form.gsm.data
        if form.email_contact.data:
            client.personne.email = form.email_contact.data

        if form2.nom.data:
            client.societe.nom = form2.nom.data
        if form2.type_societe.data:
            client.societe.type_societe = form2.type_societe.data
        if form2.domaine.data:
            client.societe.domaine = form2.domaine.data
        if form2.tel1.data:
            client.societe.tel1 = form2.tel1.data
        if form2.tel2.data:
            client.societe.tel2 = form2.tel2.data
        if form2.fax.data:
            client.societe.fax = form2.fax.data
        if form2.email.data:
            client.societe.email = form2.email.data

        db.session.commit()
        return redirect(url_for('ListClients'))
    return render_template('modifier_client.html', title='ModifierClient', form=form, form2=form2, client=client)








# user related

@login_required
@admin_required
@app.route('/CreerAgent', methods=['GET', 'POST'])
def CreerAgent():
    form = UserCreation()
    if form.validate_on_submit():
        print("form validated")
        new_personne = Personne(
            nom=form.nom.data,
            prenom=form.prenom.data,
            adresse=form.adresse.data,
            tel=form.tel.data,
            gsm=form.gsm.data,
            email=form.email.data
        )
        db.session.add(new_personne)
        db.session.commit()
        password_hash = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password=password_hash,
            privilege=form.privilege.data,
            personne_id=new_personne.id
        )
        db.session.add(new_user)
        db.session.commit()
    return render_template('creer_agent.html', title='NouveauAgent', form=form)

@login_required
@app.route('/modifier_agent/<int:id>', methods=['GET', 'POST'])
def ModifierAgent(id):
    agent = User.query.get_or_404(id)
    form = UserModification(obj = agent)
    if form.validate_on_submit():
        email_changed = form.email.data != agent.personne.email
        if form.nom.data:
            agent.personne.nom = form.nom.data
        if form.prenom.data:
            agent.personne.prenom = form.prenom.data
        if form.adresse.data:
            agent.personne.adresse = form.adresse.data
        if form.tel.data:
            agent.personne.tel = form.tel.data
        if form.gsm.data:
            agent.personne.gsm = form.gsm.data
        if form.email.data:
            agent.personne.email = form.email.data

        if form.username.data:
            agent.username = form.username.data
        
        if form.password.data:
            agent.password = generate_password_hash(form.password.data)
        
        if form.privilege.data:
            agent.privilege = form.privilege.data

        db.session.commit()
        return redirect(url_for('ListAgents'))
        
    
    return render_template('modifier_agent.html', title='ModifierAgent', form=form, agent=agent)   

@login_required
@app.route('/liste_agents')
def ListAgents():
    agents = User.query.all()
    return render_template('list_agents.html', title='Agents', agents=agents)

