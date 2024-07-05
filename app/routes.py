from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.models import User, FicheSuivi
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Avant-login')
@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

#Accueil
@app.route('/Accueil')
def Accueil():
    return render_template('Accueil.html', title='Accueil')

@app.route('/FichesSuivi')
def List_FichesSuivi():
    fiche_suivi = FicheSuivi.query.all()
    return render_template('list_prj_consulation.html', title='Fiches de suivi', fiches=fiche_suivi)