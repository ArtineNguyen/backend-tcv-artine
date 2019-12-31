from src import db

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())   
    ## RELATIONPART
    user_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False) 
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=True)

    def render(self):
        return {
            "id": self.id,
            "body": self.body,
            "author": self.author.get_data(),
            "created_at": self.created_at
        }