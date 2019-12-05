# from src import db

# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, nullable=False)
#     user = db.relationship(User)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(
#         db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
#     image_url = db.Column(db.Text)
#     view_count = db.Column(db.Integer)

# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, nullable=False)
#     user = db.relationship(User)
#     post_id = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(
#         db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())   

# db.create_all()

# @app.route('/posts/<id>', methods=['POST', 'GET'])
# def single_post(id):
#     action = request.args.get('action')
#     print(action)
#     post = Post.query.get(id)
#     if not post:
#         flash('Post not found', 'warning')
#         return redirect(url_for('root'))
#     post.author = User.query.get(post.user_id)
#     if request.method == "POST":
#         if post.user_id != current_user.id:
#             flash('not allow to do this', 'danger')
#             return redirect(url_for('root'))
#         if action == 'delete':
#             db.session.delete(post)
#             db.session.commit()
#             return redirect(url_for('root'))
#         elif action == 'update':
#             post.body = request.form['body']
#             db.session.commit()
#             return redirect(url_for('single_post', id=id))
#         elif action == 'edit':
#             return render_template('views/single_post.html', post=post, action=action)
#     if not action:
#         action = 'view'
#     comments = Comment.query.filter_by(post_id=id).all()
#     return ('Post here')


# @app.route('/posts/<id>/comment', methods=['POST', 'GET'])
# def comment(id):
#     if request.method == 'POST':
#         new_comment = Comment(user_id=current_user.id,
#                             post_id=id, body=request.form['body'])
#         db.session.add(new_comment)
#         db.session.commit()
#         return redirect(url_for('single_post', id=id, action='view'))
#     return ('Comment here')