#!/usr/bin/env python3
""" 3-app module"""

from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)
"""Babel object"""


class Config(object):
    """Configuration for Flask-Babel with available languages and defaults."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
"""class config"""


@app.route('/')
def root():
    """Render the index page with localized messages."""
    return render_template("3-index.html")


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == "__main__":
    app.run()
