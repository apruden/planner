from flask import Flask
from .model import db
from .api import api
from datetime import date
from flask.json import JSONEncoder


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.json_encoder = CustomJsonEncoder
    db.init_app(app)
    api.init_app(app)

    with app.app_context():
        db.create_all()

    return app
