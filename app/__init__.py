from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
#app.config['SQLALCHEMY DATABASE_URI'] = 'mysql://erpbet_ad:123456@localhost:3306/erpbet_db'                    
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes, models