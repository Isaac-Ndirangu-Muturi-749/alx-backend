#!/usr/bin/python3
""" 0-app module
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """hello world"""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)
