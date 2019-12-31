from src import db
from src.models.member import Member
class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey(Member.id))
    user = db.relationship(Member)
    dateEvent = db.Column(db.DateTime)
    image_url = db.Column(db.Text)
    view_count = db.Column(db.Integer)
    comments = db.relationship("Comment", backref="event", lazy=True)
    def render(self):
        return{
            "id":self.id,
            "title":self.title,
            "body":self.body,
            "image":self.image_url,
            "view_count":self.view_count,
            "user_id": self.user_id,
            "datetime": self.dateEvent,
            "comments": [comment.render() for comment in self.comments]
        }

