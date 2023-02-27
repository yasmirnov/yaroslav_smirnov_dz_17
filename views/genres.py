from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from create_data import Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

api = Api(app)
genre_ns = api.namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres_data = db.session.query(Genre)
        return genres_schema.dump(genres_data), 200

    def post(self):
        genre_data = request.json
        new_genre = Genre(**genre_data)
        db.session.add(new_genre)
        db.session.commit()
        return 'genre_added', 201


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        try:
            genre_data = db.session.query(Genre).filter(Genre.id == uid).one()
            return genre_schema.dump(genre_data), 200
        except Exception as e:
            return str(e), 404
