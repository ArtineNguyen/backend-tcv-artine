from flask import Request, Blueprint, jsonify,  request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import Post
from src import db
from flask_login import login_required, login_user, current_user, logout_user
post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/create', methods=['POST'])
def create():
    if request.method == "POST":
        data = request.get_json()
        newTitle = data['title']
        newBody = data['body']
        newImg = data['img']

        new_post = Post(title = newTitle, body = newBody, image_url = newImg)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success':False})



