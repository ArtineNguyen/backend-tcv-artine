from flask import Request, Blueprint, jsonify,request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import Member
from flask_login import login_required, login_user
member_blueprint = Blueprint('members', __name__)


@member_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        check_email = User.query.filter_by(email=request.form['email']).first()
        if check_email:  # if email taken
            flash('Email already taken', 'warning')  # we alert the user
            # then reload the register page again
            return redirect(url_for('register'))
        # if email not taken, we add new user to the database
        # we start with create an object for new_user
        new_user = User(name=request.form['name'],
                        email=request.form['email'])
        # raw password will be hashed using the generate_password method
        new_user.generate_password(request.form['password'])
        db.session.add(new_user)  # then we add new user to our session
        db.session.commit()  # then we commit to our database (kind of like save to db)
        login_user(new_user)  # then we log this user into our system
        flash('Successfully create an account and logged in', 'success')
        return redirect(url_for('root'))  # and redirect user to our root
        if current_user.is_authenticated:
            return redirect(url_for('root'))
    return render_template('views/register.html')


@member_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        frontend_email = data['email']
        frontend_password = data['password']
        check_email = Member.query.filter_by(email=frontend_email).first()
        
        if check_email: # neu co email
            if check_email.check_password(frontend_password):
                login_user(check_email)
                return jsonify({
                    "success": True,
                    "user":{
                        "name": check_email.name,
                        "email": check_email.email,
                        "id": check_email.id
                    }
                })
            else: return jsonify({"success": False})
        else: return jsonify({"success": False})
    return jsonify({"success": False})


@member_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@member_blueprint.route('/')
@login_required
def root():
    # query posts from database
    posts = Post.query.all()
    # modify our posts so that each post will include all author info:
    for post in posts:
        post.author = User.query.filter_by(id=post.user_id).first()
    return render_template('views/index.html', posts=posts)