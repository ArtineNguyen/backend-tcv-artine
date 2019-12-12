from flask import Request, Blueprint, jsonify,request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import Member,Token
from flask_login import login_required, login_user, current_user, logout_user
member_blueprint = Blueprint('members', __name__)
import uuid
from src import app, db
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer

@member_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        frontend_email = data['email']
        frontend_password = data['password']
        check_email = Member.query.filter_by(email=frontend_email).first()
        
        if check_email: # neu co email
            if check_email.check_password(frontend_password):
                token = Token.query.filter_by(user_id=check_email.id).first()
                if not token:
                    token = Token(user_id=check_email.id,
                                  uuid=str(uuid.uuid4().hex))
                    db.session.add(token)
                    db.session.commit()
                login_user(check_email)
                return jsonify({
                    "success": True,
                    "user":{
                        "name": check_email.name,
                        "email": check_email.email,
                        "id": check_email.id,                       
                    },
                    'token': token.uuid
                })
            else: return jsonify({"success": False})
        else: return jsonify({"success": False})
    return jsonify({"success": False})


@member_blueprint.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id=current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    logout_user()
    return jsonify({
        'success': True
    })

@member_blueprint.route('/getuser', methods=['GET'])
@login_required
def get_user():
    return jsonify({
        "name": current_user.name,
        "id": current_user.id,
        "email": current_user.email
    })

@member_blueprint.route('/register', methods=['POST'])
def register_user():
    if request.method=='POST':

        data = request.get_json()
        print(data,"GHUJKL:HGJHKJ")
        userEmail = data['email']
        userPassword = data['password']
        userName = data['name']
        user = Member.query.filter_by(email = userEmail).first()
        if user:
            return jsonify({'message':'Email already exist!'})
        else :
            new_user = Member(email = userEmail, name = userName)
            new_user.generate_password(userPassword)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'You has sign up, please login!'})

def send_email(token, email, name):
    with app.app_context():
        try:
            msg = Message(subject="Reset your password from The Cancer Voice",
                        sender=app.config.get("MAIL_USERNAME"), #sender email
                        recipients=[email],
                        body= f"Hi {name}! Thanks for comeback with us! To reset your email please enter the link : http://localhost:3000/new-password/?token=${token}")
            mail.send(msg)
        except Exception as err:
            print(f'{err}')
        else: print("success!")

@member_blueprint.route('/forgot-password', methods = ['POST'])
def get_password():
    if request.method == 'POST':
        data = request.get_json()
        user = Member.query.filter_by(email = data['email']).first()
        if not user:
            return jsonify({'success': False,
                            'wrong': 'Email does not exist'}
            )
        else:
            s = URLSafeTimedSerializer(app.secret_key)
            token = s.dumps(user.email, salt="RESET_PASSWORD")
            send_email(token, user.email, user.name)
            return jsonify({"success": True, 'right': 'Email has sent'})
    return jsonify({'success': False, 'state': 'Please input your email'})