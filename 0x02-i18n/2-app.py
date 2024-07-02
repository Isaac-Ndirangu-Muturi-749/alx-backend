#!/usr/bin/python3
""" 1-app module"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration for Flask-Babel with available languages and defaults."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the index page."""
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(debug=True)
