#!/usr/bin/python3
"""app module"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from datetime import datetime


class Config:
    """Configuration for Flask-Babel with available languages and defaults."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns a user dictionary or None if the ID is not found
    or not passed."""
    login_as = request.args.get('login_as')
    if login_as:
        user_id = int(login_as)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """Executed before each request to set the user in flask.g."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages,
    or use URL parameter."""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine the best match for supported timezones,
    or use URL parameter."""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass
    if g.user:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Render the index page with localized messages and current time."""
    current_time = datetime.now(pytz.timezone(
        get_timezone())).strftime('%b %d, %Y, %I:%M:%S %p')
    return render_template('7-index.html', current_time=current_time)


if __name__ == '__main__':
    app.run(debug=True)
