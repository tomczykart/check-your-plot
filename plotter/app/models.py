from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    searched_plots = db.relationship('search_query', backref='author', lazy='dynamic')
#define function when instance is called
    def __repr__(self):
        return f'<User: {self.email}>'

class search_query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plot_id = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_created = db.Column(db.DateTime(timezone=True), index=True, server_default=db.func.now())
#define function when instance is called
    def __repr__(self):
        return f'<Searched query: {self.plot_id}>'
