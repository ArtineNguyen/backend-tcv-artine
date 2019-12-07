from flask import Request, Blueprint, jsonify,request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import Member,Token
from flask_login import login_required, login_user, current_user, logout_user
member_blueprint = Blueprint('members', __name__)
import uuid
from src import app, db


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