from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo, Email
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=45)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=45)])
    submit = SubmitField('Sign In')

class UserModification(FlaskForm):
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    username = StringField('Username')
    adresse = StringField('Adresse')
    tel = StringField('Tel')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Modifier utilisateur')
    
    def validate_password(self, field):
        if field.data and not self.confirm_password.data:
            raise ValidationError('Please confirm your password.')
        if self.confirm_password.data and not field.data:
            raise ValidationError('Please enter a password.')
        
class ProjectCreation(FlaskForm):
    nom = StringField('Projet')
    adresse = StringField('Adresse')
    agent = SelectField('Agent', choices=[], validators=[DataRequired()])

class ClientCreation(FlaskForm):
    nom = StringField('Nom')
    type_societe = StringField('Type société')
    domaine = StringField('Domaine')
    tel1 = StringField('Tel1')
    tel2 = StringField('Tel2')
    fax = StringField('Fax')
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
    