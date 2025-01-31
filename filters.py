from datetime import datetime
from flask import Flask


def register_template_filters(app: Flask) -> None:
    """Register custom template filters for the Flask application."""

    @app.template_filter('length')
    def length_filter(value):
        """Return the length of an object that supports len()"""
        return len(value)
    
    @app.template_filter('filter_shows')
    def upcoming_filter(value, upcoming:bool = True):
        upcoming_shows = []
        past_shows = []
        current_time = datetime.now()

        for show in value.shows:
            if show.start_time > current_time:
                upcoming_shows.append(show)
            else:
                past_shows.append(show)
        if upcoming:
            return upcoming_shows
        else:
            return past_shows

    @app.template_filter('format_datetime')
    def format_datetime(value):
        """Format datetime object to string"""
        if isinstance(value, str):
            try:
                date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    date = datetime.fromisoformat(value)
                except ValueError:
                    return value
        else:
            date = value
        return date.strftime('%Y-%m-%d %H:%M:%S')