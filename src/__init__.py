from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_cors import CORS
from flask_mail import Mail
import os
app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = "super"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)

db.init_app(app)

migrate = Migrate(app, db)
CORS(app)
from src.models import Member, Token

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return Member.query.get(id)


mail_setting = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_setting)
mail = Mail(app)

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None

from src.components.member import member_blueprint
app.register_blueprint(member_blueprint, url_prefix="/")

from src.components.post import post_blueprint
app.register_blueprint(post_blueprint, url_prefix="/post")

from src.components.post import post_blueprint
app.register_blueprint(post_blueprint, url_prefix="/post/comment")

from src.components.oauth import blueprint
app.register_blueprint(blueprint, url_prefix="/loginfacebook")

from src.components.event import event_blueprint
app.register_blueprint(event_blueprint, url_prefix="/event")