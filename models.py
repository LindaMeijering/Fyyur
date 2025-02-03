from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

venue_genres = db.Table('venue_genres',
                        db.Column('venue_id', db.Integer, db.ForeignKey(
                            'venue.id'), primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey(
                            'genre.id'), primary_key=True)
                        )

artist_genres = db.Table('artist_genres',
                         db.Column('artist_id', db.Integer, db.ForeignKey(
                             'artist.id'), primary_key=True),
                         db.Column('genre_id', db.Integer, db.ForeignKey(
                             'genre.id'), primary_key=True)
                         )


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<Genre {self.name}>'


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    venues = db.relationship('Venue', backref='area', lazy=True)
    artists = db.relationship('Artist', backref='area', lazy=True)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String, nullable=True)
    website = db.Column(db.String, nullable=False)
    genres = db.relationship(
        'Genre', secondary=venue_genres, backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue {self.name}>'


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)
    genres = db.relationship(
        'Genre', secondary=artist_genres, backref='artists', lazy=True)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
