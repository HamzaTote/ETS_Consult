from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField, FloatField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo, Email, Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=45)])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=8, max=45)])
    submit = SubmitField('Connexion')

class UserModification(FlaskForm):
    nom = StringField('Nom', validators=[Optional()])
    prenom = StringField('Prenom', validators=[Optional()])
    username = StringField('Username', validators=[Optional()])
    adresse = StringField('Adresse', validators=[Optional()])
    tel = StringField('Tel', validators=[Optional()])
    gsm = StringField('GSM', validators=[Optional()])
    email = StringField('Email', validators=[Email(), Optional()])
    password = PasswordField('Mot de passe', validators=[Optional()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[EqualTo('password', message='Les mots de passe doivent être similaires.'), Optional()])
    privilege = SelectField('Privilège', choices=[('admin','admin'), ('agent','agent')], validators=[Optional()])
    submit = SubmitField('Modifier utilisateur')
    
    def validate_password(self, field):
        min_length = 8

        if field.data and not self.confirm_password.data:
            raise ValidationError('Please confirm your password.')
        if self.confirm_password.data and not field.data:
            raise ValidationError('Please enter a password.')
        if len(field.data) < min_length:
            raise ValidationError(f'Password must be at least {min_length} characters long.')

        if field.data != self.confirm_password.data:
            raise ValidationError('Passwords must match.')
        
class ProjectCreation(FlaskForm):
    nom = StringField('Projet', validators=[DataRequired()])
    adresse = StringField('Adresse')
    agent = SelectField('Agent', choices=[], validators=[DataRequired()])
    client = SelectField('Client', choices=[], validators=[DataRequired()])
    submit = SubmitField('Créer')

class SocieteCreation(FlaskForm):
    nom = StringField('Nom')
    type_societe = StringField('Type société')
    domaine = StringField('Domaine')
    tel1 = StringField('Tel1')
    tel2 = StringField('Tel2')
    fax = StringField('Fax')
    email = StringField('Email')

class ContactCreation(FlaskForm):
    nom_contact = StringField('Nom')
    prenom = StringField('Prenom')
    adresse = StringField('Adresse')
    tel = StringField('Tel')
    gsm = StringField('GSM')
    email_contact = StringField('Email')
    
class UserCreation(FlaskForm):
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    adresse = StringField('Adresse')
    tel = StringField('Tel')
    gsm = StringField('GSM')
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password')
    privilege = SelectField('Privilege', choices=[('admin', 'admin'), ('agent', 'agent')])
    submit = SubmitField('Créer')
    

class PrestationCreation(FlaskForm):
    type = SelectField('Type', choices=[('Diagnostic', 'Diagnostic'), ('Etudes techniques', 'Etudes techniques'), ('Essais', 'Essais'), ('Etude géotechnique', 'Etude géotechnique'), ('Expertise', 'Expertise'), ('Evaluation', 'Evaluation'), ('Audit', 'Audit'), ('Suivi et réception des travaux', 'Suivi et réception des travaux')], validators=[DataRequired()])
    titre = StringField('Titre', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    code = StringField('Code', validators=[Optional()])
    submit = SubmitField('Créer')


class ProjetModification(FlaskForm):
    nom = StringField('Projet', validators=[Optional()])
    adresse = StringField('Adresse', validators=[Optional()])
    agent = SelectField('Agent', choices=[], validators=[Optional()])
    submit = SubmitField('Créer')

class SocieteModification(FlaskForm):
    nom = StringField('Nom', validators=[Optional()])
    type_societe = StringField('Type société', validators=[Optional()])
    domaine = StringField('Domaine', validators=[Optional()])
    tel1 = StringField('Tel1', validators=[Optional()])
    tel2 = StringField('Tel2', validators=[Optional()])
    fax = StringField('Fax', validators=[Optional()])
    email = StringField('Email', validators=[Email(), Optional()])

class ContactModification(FlaskForm):
    nom_contact = StringField('Nom', validators=[Optional()])
    prenom = StringField('Prenom', validators=[Optional()])
    adresse = StringField('Adresse', validators=[Optional()])
    tel = StringField('Tel', validators=[Optional()])
    gsm = StringField('GSM', validators=[Optional()])
    email_contact = StringField('Email', validators=[Email(), Optional()])

class DevisCreation(FlaskForm):
    objet = StringField('Objet', validators=[DataRequired()])
    generalites = StringField('Généralités', validators=[DataRequired()])
    prestation = SelectField('Prestation', choices=[], validators=[DataRequired()])
    montant_ttc = FloatField('Total TTC', validators=[DataRequired()])
    submit = SubmitField('Créer')


class PrestationVF(FlaskForm):
    unite = SelectField('Unité', validators=[DataRequired()], choices=[('m²', 'm²'), ('m³', 'm³'), ('F', 'F'), ('U', 'U'), ('V', 'V')])
    quantite = IntegerField('Quantité', validators=[DataRequired()])
    prix_unitaire = FloatField('Prix unitaire', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

