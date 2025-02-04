from sqlalchemy.exc import SQLAlchemyError

from models import Area, Genre


def get_or_create_area(city, state, db):
    area = Area.query.filter_by(city=city, state=state).first()
    if not area:
        area = Area(city=city, state=state)
        db.session.add(area)
        db.session.flush()
    return area


def get_or_create_genre(genre_name, db):
    try:
        genre = Genre.query.filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.session.add(genre)
            db.session.flush()
        return genre
    except SQLAlchemyError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise
