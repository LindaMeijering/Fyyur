# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import logging
import secrets
from logging import FileHandler, Formatter

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from filters import register_template_filters
from forms import *
from models import db, Genre, Area, Venue, Artist, Show

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# Replace with a real secret key
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
# Optional separate CSRF key
# app.config['WTF_CSRF_SECRET_KEY'] = secrets.token_urlsafe(32)
register_template_filters(app)
db.init_app(app)

migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    areas = Area.query.all()
    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    data = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


logger = logging.getLogger(__name__)

def _get_or_create_area(city, state):
    area = Area.query.filter_by(city=city, state=state).first()
    if not area:
        area = Area(city=city, state=state)
        db.session.add(area)
        db.session.flush()
    return area

def _get_or_create_genre(genre_name):
    try:
        genre = Genre.query.filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.session.add(genre)
            db.session.flush()
        return genre
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(
            f"Database error creating genre '{genre_name}': {str(e)}")
        raise
    except Exception as e:
        db.session.rollback()
        logger.error(
            f"Unexpected error creating genre '{genre_name}': {str(e)}")
        raise
class CreationService:
    def __init__(self, db):
        self.db = db

    def create_venue(self, form):
        try:
            area = _get_or_create_area(form.city.data, form.state.data)

            venue = Venue(
                name=form.name.data,
                address=form.address.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                website=form.website_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
                area_id=area.id
            )
            self.db.session.add(venue)

            for genre_name in form.genres.data:
                genre = _get_or_create_genre(genre_name)
                venue.genres.append(genre)

            self.db.session.commit()
            return venue

        except SQLAlchemyError as e:
            self.db.session.rollback()
            logger.error(f"Database error creating venue: {str(e)}")
            raise
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Unexpected error creating venue: {str(e)}")
            raise

    def create_artist(self, form):
            try:
                area = _get_or_create_area(
                    form.city.data, form.state.data)

                artist = Artist(
                    name=form.name.data,
                    phone=form.phone.data,
                    image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_venue=form.seeking_venue.data,
                    seeking_description=form.seeking_description.data,
                    area_id=area.id
                )
                self.db.session.add(artist)

                for genre_name in form.genres.data:
                    genre = _get_or_create_genre(genre_name)
                    artist.genres.append(genre)

                self.db.session.commit()
                return artist

            except SQLAlchemyError as e:
                self.db.session.rollback()
                logger.error(f"Database error creating venue: {str(e)}")
                raise
            except Exception as e:
                self.db.session.rollback()
                logger.error(f"Unexpected error creating venue: {str(e)}")
                raise


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()

    if form.validate_on_submit():
        service = CreationService(db)
        try:
            venue = service.create_venue(form)
            flash(f'Venue {venue.name} was successfully listed!')
            return redirect(url_for('show_venue', venue_id=venue.id))
        except Exception as e:
            flash(
                f'An error occurred. Venue {form.name.data} could not be listed.')
            logger.error(f"Venue creation failed: {str(e)}")
            return redirect(url_for('create_venue_form'))

    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {field}: {error}')
    return redirect(url_for('create_venue_form'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        return jsonify({'success': True}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        db.session.close()

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    data = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    form.city.data = artist.area.city
    form.state.data = artist.area.state
    form.genres.data = [genre.name for genre in artist.genres]

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    try:
        artist.name = form.name.data
        artist.phone = form.phone.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        artist.area_id = _get_or_create_area(
            city=form.city.data, state=form.state.data).id

        artist.genres.clear()
        for genre_name in form.genres.data:
            genre = _get_or_create_genre(genre_name=genre_name)
            if genre not in artist.genres:
                artist.genres.append(genre)

        db.session.commit()
        return render_template('pages/show_artist.html', artist=artist)

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error updating artist: %s", str(e))
        raise

    except Exception as e:
        db.session.rollback()
        logger.error("Unexpected error updating artist: %s", str(e))
        raise

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    form.city.data = venue.area.city
    form.state.data = venue.area.state
    form.genres.data = [genre.name for genre in venue.genres]
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()

    if form.validate_on_submit():
        service = CreationService(db)
        try:
            artist = service.create_artist(form)
            flash(f'Artist {artist.name} was successfully listed!')
            return redirect(url_for('show_artist', artist_id=artist.id))
        except Exception as e:
            flash(
                f'An error occurred. Artist {form.name.data} could not be listed.')
            logger.error(f"Artist creation failed: {str(e)}")
            return redirect(url_for('create_artist_form'))

    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {field}: {error}')
    return redirect(url_for('create_artist_form'))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = Show.query.all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
