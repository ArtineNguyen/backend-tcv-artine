from flask import Request, Blueprint, jsonify,  request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import Event
from src import db
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime

event_blueprint = Blueprint('events', __name__)

@event_blueprint.route('/render-event')
def render():
    return jsonify([event.render() for event in Event.query.all()])

@event_blueprint.route('/create-event', methods=['POST'])
@login_required
def create_event():
    if request.method == "POST":
        data = request.get_json()
        newTitle = data['title']
        newBody = data['body']
        newImg = data['img']
        newYear = int(data['year'])
        newMonth = int(data['month'])
        newDay = int(data['day'])
        newHour = int(data['hour'])
        newMinute = int(data['minute'])
        print(newTitle, 'title here')
        new_event = Event(title = newTitle, body = newBody, image_url = newImg, user_id = current_user.id, dateEvent = datetime(newYear, newMonth, newDay, newHour, newMinute, 0, 0))
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success':False})

@event_blueprint.route('/event/<id>/comment', methods=['POST', 'GET'])
def comment_event(id):
    if request.method == 'POST':
        new_comment = Comment(user_id=current_user.id,
                            event_id=id, body=request.form['event_body'])
        db.session.add(new_comment_event)
        db.session.commit()
        return redirect(url_for('single_event', id=id, action='view'))
    return ('Comment Event here')

@event_blueprint.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete_event(id):
    if request.method == "DELETE":
        event_delete = Event.query.filter_by(id =id).first()
        db.session.delete(event_delete)
        db.session.commit()
        return jsonify({'session': True})
    return jsonify({'session': False})

@event_blueprint.route('/single-event/<id>')
def single_event(id):
    single = Event.query.filter_by(id = id).first()
    return jsonify({
        "title": single.title,
        "body": single.body,
        "img": single.image_url,
        "userID": single.user_id,
        "datetime": single.dateEvent
    })

@event_blueprint.route('/change/<id>', methods=['PUT'])
@login_required
def change_event(id):
    if request.method == 'PUT':
        event_change = Event.query.filter_by(id = id).first()
        data = request.get_json()
        editTitle = data['title']
        editBody = data['body']
        editImg = data['img']
        newYear = int(data['year'])
        newMonth = int(data['month'])
        newDay = int(data['day'])
        newHour = int(data['hour'])
        newMinute = int(data['minute'])
        event_change.title = editTitle
        event_change.body = editBody
        event_change.image_url = editImg
        event_change.dateEvent = datetime(newYear, newMonth, newDay, newHour, newMinute, 0, 0)

        db.session.commit()
        return jsonify({'success': True})
    return jsonify({"success": False})