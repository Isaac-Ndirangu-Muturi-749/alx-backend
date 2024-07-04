#!/usr/bin/python3
""" 4-app module"""

from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """Configuration for Flask-Babel with available languages and defaults."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
"""class config"""


babel = Babel(app)
"""Babel object"""


@babel.localeselector
def get_locale():
    """ to determine the best match with our supported languages """
    localLang = request.args.get('locale')
    supportLang = app.config['LANGUAGES']
    if localLang in supportLang:
        return localLang
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the index page with localized messages."""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
