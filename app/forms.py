from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo, Email, Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=45)])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=8, max=45)])
    submit = SubmitField('Connexion')

class UserModification(FlaskForm):
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    username = StringField('Username')
    adresse = StringField('Adresse')
    tel = StringField('Tel')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords must match.')])
    privilege = SelectField('Privilege', choices=[('admin','admin'), ('agent','agent')])
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
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    adresse = StringField('Adresse')
    tel = StringField('Tel')
    gsm = StringField('GSM')
    email = StringField('Email')
    
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
    type = SelectField('Type', choices=[('Diagnostic', 'Diagnostic'), ('Etudes techniques', 'Etudes techniques'), ('Essais', 'Essais'), ('Etude géotechnique', 'Etude géotechnique'), ('Expertise', 'Expertise'), ('Evaluation', 'Evaluation'), ('Audit', 'Audit'), ('Suivi et réception des travaux', 'Suivi et réception des travaux')])
    description = StringField('Description')
    code = StringField('Code', validators=[Optional()])
    submit = SubmitField('Créer')