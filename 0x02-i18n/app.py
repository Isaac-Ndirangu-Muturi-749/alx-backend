#!/usr/bin/env python3
"""app module"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
import datetime

app = Flask(__name__)
babel = Babel(app)
"""Babel object"""
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Configuration for Flask-Babel with available languages and defaults."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
"""class config"""


@app.route('/')
def root():
    """Render the index page with localized messages and current time."""
    return render_template("index.html")


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages,
    or use URL parameter."""
    localLang = request.args.get('locale')
    supportLang = app.config['LANGUAGES']
    if localLang in supportLang:
        return localLang
    userId = request.args.get('login_as')
    if userId:
        localLang = users[int(userId)]['locale']
        if localLang in supportLang:
            return localLang
    localLang = request.headers.get('locale')
    if localLang in supportLang:
        return localLang
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """Returns a user dictionary or None if the ID is not found
    or not passed."""
    try:
        userId = request.args.get('login_as')
        return users[int(userId)]
    except Exception:
        return None


@app.before_request
def before_request():
    """Executed before each request to set the user in flask.g."""
    g.user = get_user()
    utcNow = pytz.utc.localize(datetime.datetime.utcnow())
    local_time_now = utcNow.astimezone(pytz.timezone(get_timezone()))


@babel.timezoneselector
def get_timezone():
    """Determine the best match for supported timezones,
    or use URL parameter."""
    localTimezone = request.args.get('timezone')
    if localTimezone:
        if localTimezone in pytz.all_timezones:
            return localTimezone
        else:
            raise pytz.exceptions.UnknownTimeZoneError
    try:
        userId = request.args.get('login_as')
        user = users[int(userId)]
        localTimezone = user['timezone']
    except Exception:
        localTimezone = None
    if localTimezone:
        if localTimezone in pytz.all_timezones:
            return localTimezone
        else:
            raise pytz.exceptions.UnknownTimeZoneError
    return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == "__main__":
    app.run()
