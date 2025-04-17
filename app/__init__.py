import os
import urllib.request
import json

from flask import Flask
from prometheus_client import Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Set a few globals here
height = Gauge('height', 'River height')
height.set(1.2)

def get_river_height(siteCode="02333500"):
    waterservices_url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=%s&siteStatus=all'% siteCode
    with urllib.request.urlopen(waterservices_url) as response:
        json_response = response.read()

    stats = json.loads(json_response)
    variable = None
    value = None
    
    for v in stats['value']['timeSeries']:
        if v['variable']['variableCode'][0]['value'] == "00065":
            variable = v
            value = v['values'][0]['value'][0]['value']

    height.set(float(value))
    
    return value

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Return the river height
    @app.route('/height')
    def height():
        html = get_river_height()
        return html

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Add prometheus wsgi middleware to route /metrics requests
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    return app

    
