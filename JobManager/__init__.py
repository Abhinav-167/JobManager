from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from oauthlib.oauth2 import WebApplicationClient
import os

from flask_socketio import SocketIO, send
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized
app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = b"Y\xb6\xb0T<)=\x86'\xee\xb2\xf7\xd3!\xe6\xc4\t\xac\x7fY\xf7r\xb1O"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'babhinav.117@gmail.com'
app.config['MAIL_PASSWORD'] = 'hrddruwxjhssnhzj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
mail = Mail(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
socketio = SocketIO(app)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from JobManager import routes, models, google_login
