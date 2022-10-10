from app import db
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    searched_plots = db.relationship('SearchQuery', backref='author', lazy='dynamic')
#define text representation when instance is called
    def __repr__(self):
        return f'<User id: {self.id}, and email: {self.email}>'


class SearchQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plot_id = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_created = db.Column(db.DateTime(timezone=True), index=True, server_default=db.func.now())
#define text representation when instance is called
    def __repr__(self):
        return f'<Searched query: {self.plot_id}>'
