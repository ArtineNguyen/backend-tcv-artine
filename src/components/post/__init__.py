from flask import Request, Blueprint, jsonify,  request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import Post
from src import db
from flask_login import login_required, login_user, current_user, logout_user

post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/render-post')
def render():
    return jsonify([post.render() for post in Post.query.all()])

@post_blueprint.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json()
        newTitle = data['title']
        newBody = data['body']
        newImg = data['img']
        new_post = Post(title = newTitle, body = newBody, image_url = newImg, user_id = current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success':False})

@post_blueprint.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete_post(id):
    if request.method == 'DELETE':
        post_need_to_delete = Post.query.filter_by(id = id).first()

        db.session.delete(post_need_to_delete)
        db.session.commit()
        return jsonify({"success": True})

@post_blueprint.route('/edit-post/<id>', methods=['PUT'])
@login_required
def edit_post(id):
    if request.method == "PUT":
        data = request.get_json()
        editTitle = data['title']
        editBody = data['body']
        editImg = data['img']
        edit_post = Post.query.filter_by(id = id). first()

        edit_post.title = editTitle
        edit_post.body = editBody
        edit_post.image_url = editImg

        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success':False})

@post_blueprint.route("/single-post/<id>")
def single_post(id):
    singel = Post.query.filter_by(id = id).first()
    return jsonify({'title': singel.title,
                    'body': singel.body,
                    'img': singel.image_url,
                    "userid": singel.user_id
                    })


# @post_blueprint.route('/posts/<id>/comment', methods=['POST', 'GET'])
# def comment_post(id):
#     if request.method == 'POST':
#         new_comment = Comment(user_id=current_user.id,
#                             post_id=id, body=request.form['body'])
#         db.session.add(new_comment_post)
#         db.session.commit()
#         return redirect(url_for('single_post', id=id, action='view'))
#     return ('Comment Post here')



