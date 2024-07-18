from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import check_password_hash, generate_password_hash

Base = db.Model

class Personne(Base):
    __tablename__ = 'personne'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(45), index=True)
    prenom = db.Column(db.String(45), index=True)
    adresse = db.Column(db.String(100), index=True, unique=True)
    tel = db.Column(db.String(10), index=True, unique=True)
    gsm = db.Column(db.String(10), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    profession = db.Column(db.String(45), index=True)
    societe_id = db.Column(db.Integer, ForeignKey('societe.id'), nullable=True)
    poste_societe = db.Column(db.String(45), index=True)
    user = relationship('User', uselist=False, back_populates='personne')
    #agent = relationship('Agent', uselist=False, back_populates='personne')
    client = relationship('Client', uselist=False, back_populates='personne')

    def __repr__(self):
        return f'<Personne {self.id} - {self.email}>'

class User(UserMixin, Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), index=True, unique=True)
    password = db.Column(db.String(255), index=True, unique=True)
    personne_id = db.Column(db.Integer, ForeignKey('personne.id'), nullable=False)
    #agent_id = db.Column(db.Integer, ForeignKey('agent.id'), nullable=False)
    privilege = db.Column(db.String(10), nullable=False)
    personne = relationship('Personne', uselist=False, back_populates='user')
    #agent = relationship('Agent', uselist=False, back_populates='user')
    fiche_suivi = relationship('FicheSuivi', back_populates='user')

    __table_args__ = (
        CheckConstraint("privilege IN ('admin', 'agent')", name='check_user_privilege'),
    )

    def __repr__(self):
        return f'<User {self.id} - {self.email}>'
    
    def add_user(self,nom, prenom, username, password, privilege):
        if self.privilege == 'admin':
            return User(nom, prenom, username=username, password=password, privilege=privilege)
        
    def modify_user(self, nom, prenom, username, password, privilege):
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.password = password
        self.privilege = privilege
        return self

    

# class Agent(Base):
#     __tablename__ = 'agent'
#     id = db.Column(db.Integer, primary_key=True)
#     code_agent = db.Column(db.String(45), index=True, unique=True)
#     personne_id = db.Column(db.Integer, ForeignKey('personne.id'), nullable=False)
#     personne = relationship('Personne', uselist=False, back_populates='agent')
#     user = relationship('User', uselist=False, back_populates='agent')
#     fiche_suivi = relationship('FicheSuivi', back_populates='societe')

#     def __repr__(self):
#         return f'<Agent {self.id}>'

class Client(Base):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    societe_id = db.Column(db.Integer, ForeignKey('societe.id'), nullable=True)
    personne_id = db.Column(db.Integer, ForeignKey('personne.id'), nullable=False)
    personne = relationship('Personne', uselist=False, back_populates='client')
    societe = relationship('Societe', uselist=False, back_populates='client')
    fiche_suivi = relationship('FicheSuivi', back_populates='client')

    __table_args__ = (
        CheckConstraint('societe_id IS NOT NULL OR personne_id IS NOT NULL', name='check_societe_personne_not_both_null'),
    )

    def __repr__(self):
        return f'<Client {self.id}>'
    
    def get_client_id(self):
        if self.societe:
            return self.societe.id
        elif self.personne:
            return self.personne.id
        else:
            return None

class Societe(Base):
    __tablename__ = 'societe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(45), index=True, unique=True)
    type_societe = db.Column(db.String(45), index=True)
    domaine = db.Column(db.String(45), index=True)
    tel1 = db.Column(db.String(45), index=True, unique=True)
    tel2 = db.Column(db.String(45), index=True, unique=True)
    fax = db.Column(db.String(45), index=True, unique=True)
    email = db.Column(db.String(45), index=True, unique=True)
    client = relationship('Client', uselist=False, back_populates='societe')

    def __repr__(self):
        return f'<Societe {self.id} - {self.nom}>'

# class Projet(Base):
#     __tablename__ = 'projet'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     nom = db.Column(db.String(200), index=True, unique=True)
#     adresse = db.Column(db.String(45), index=True, unique=True)
#     client_id = db.Column(db.Integer, ForeignKey('client.id'))
#     fiche_suivi = relationship('FicheSuivi', back_populates='projet')

#     def __repr__(self):
#         return f'<Projet {self.id} - {self.nom}>'

class FicheSuivi(Base):
    __tablename__ = 'fiche_suivi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FSN = db.Column(db.String(7), index=True, unique=True)
    projet = db.Column(db.String(255), index=True, unique=True)
    adresse = db.Column(db.String(255), index=True, unique=True)
    prestation_id = db.Column(db.Integer, ForeignKey('prestation.id'))
    ouvrage_id = db.Column(db.Integer, ForeignKey('ouvrage.id'))
    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    date_debut = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    client = relationship('Client', back_populates='fiche_suivi')
    user = relationship('User', back_populates='fiche_suivi')
    devis = relationship('Devis', back_populates='fiche_suivi')

    def __repr__(self):
        return f'<FicheSuivi {self.id}>'
    
    @classmethod
    def generate_fsn(self):
        current_year = datetime.now().year % 100
        last_project = FicheSuivi.query.filter(FicheSuivi.FSN.endswith(f'/{current_year}')).order_by(FicheSuivi.id.desc()).first()
    
        if last_project:
            last_fsn_number = int(last_project.FSN.split('/')[0])
            new_fsn_number = last_fsn_number + 1
        else:
            new_fsn_number = 1

        new_fsn = f'{new_fsn_number:02d}/{current_year}'
        return new_fsn

class Prestation(Base):
    __tablename__ = 'prestation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_prestation = db.Column(db.String(45), index=True)
    code = db.Column(db.String(45), index=True, unique=True)

    def __repr__(self):
        return f'<Prestation {self.id}>'

class Ouvrage(Base):
    __tablename__ = 'ouvrage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_ouvrage = db.Column(db.String(45), index=True)
    code = db.Column(db.String(45), index=True, unique=True)

    def __repr__(self):
        return f'<Ouvrage {self.id}>'

class Dossier(Base):
    __tablename__ = 'dossier'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String(45), index=True, unique=True)
    annee = db.Column(db.Integer, index=True)
    fiche_suivi_id = db.Column(db.Integer, ForeignKey('fiche_suivi.id'))

    def __repr__(self):
        return f'<Dossier {self.id}>'


#Documents

class Devis(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String(45), index=True, unique=True)
    fiche_suivi_id = db.Column(db.Integer, ForeignKey('fiche_suivi.id'))
    date = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    montant = db.Column(db.Float, index=True)
    fiche_suivi = relationship('FicheSuivi', back_populates='devis')
    