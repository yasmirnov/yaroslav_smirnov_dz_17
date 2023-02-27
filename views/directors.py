from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from create_data import Director

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

api = Api(app)
director_ns = api.namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors_data = db.session.query(Director)
        return directors_schema.dump(directors_data), 200

    def post(self):
        director_data = request.json
        new_director = Director(**director_data)
        db.session.add(new_director)
        db.session.commit()
        return 'director_added', 201


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid: int):
        try:
            director_data = db.session.query(Director).filter(Director.id == uid).one()
            return director_schema.dump(director_data), 200
        except Exception as e:
            return str(e), 404
