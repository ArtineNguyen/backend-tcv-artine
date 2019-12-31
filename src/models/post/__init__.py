from src import db
from src.models.member import Member
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Member.id))
    user = db.relationship(Member)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())
    image_url = db.Column(db.Text)
    view_count = db.Column(db.Integer)
    ### RELATION PART
    comments = db.relationship("Comment", backref="post", lazy=True)

    def render(self):
        return{
            "id":self.id,
            "title":self.title,
            "body":self.body,
            "image":self.image_url,
            "created_at":self.created_at,
            "updated_at":self.updated_at,
            "view_count":self.view_count,
            "user_id": self.author.get_data(),
            "comments": [comment.render() for comment in self.comments[::-1]]
        }

