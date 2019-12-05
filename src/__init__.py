from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__)


app.config.from_object('config.Config')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'something'
db=SQLAlchemy(app)


from src.models import Member
from src.components.cli import create_db
app.cli.add_command(create_db)
migrate = Migrate(app, db)
CORS(app)

login_manager = LoginManager(app)
from src.components.member import member_blueprint
app.register_blueprint(member_blueprint, url_prefix="/")