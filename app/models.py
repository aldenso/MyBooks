from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id) #python3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    fullname = db.Column(db.String(100))
    biography = db.Column(db.Text(200))
    books = db.relationship('Book', backref='authorbook', lazy='dynamic')

    def __repr__(self):
        return '<Author: %r %r>' % (self.firstname, self.lastname)

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description =db.Column(db.Text(140))
    books = db.relationship('Book', backref='publisherbook', lazy='dynamic')

    def __repr__(self):
        return '<Publisher: %r>' % (self.name)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(140))
    synopsis = db.Column(db.Text(200))
    year = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))

    def __repr__(self):
        return '%r' % (self.title)
