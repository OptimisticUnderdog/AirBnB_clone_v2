#!/usr/bin/python3
"""
Configures content to serve on port 5000
"""

from flask import Flask

app = Flask(__name__)


@app.route('/airbnb-onepage/', methods=['GET'])
def hello_route():
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
