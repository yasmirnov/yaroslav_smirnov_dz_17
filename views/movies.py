from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from create_data import Movie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        try:
            if director_id and genre_id:
                movies_by_filters = db.session.query(Movie).filter(Movie.director_id == director_id).filter(Movie.genre_id == genre_id).all()
                if movies_by_filters:
                    return movies_schema.dump(movies_by_filters), 200
                return 'movies not found for this query'
            return 'director_id or genre_id missing'
        except Exception as e:
            return str(e), 404

    def post(self):
        movie_data = request.json
        new_movie = Movie(**movie_data)
        db.session.add(new_movie)
        db.session.commit()
        return 'movie_added', 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie_data = db.session.query(Movie).filter(Movie.id == uid).one()
            return movie_schema.dump(movie_data), 200
        except Exception as e:
            return str(e), 404

    def put(self, uid: int):
        data = request.json
        movie_data = db.session.query(Movie).filter(Movie.id == uid).one()
        movie_data.title = data.get('title')
        movie_data.description = data.get('description')
        movie_data.trailer =data.get('trailer')
        movie_data.year = data.get('year')
        movie_data.rating = data.get('rating')
        movie_data.genre_id = data.get('genre_id')
        movie_data.director_id = data.get('director_id')

        db.session.add(movie_data)
        db.session.commit()

        return 'movie_changed', 204

    def delete(self, uid: int):
        movie_data = db.session.query(Movie).filter(Movie.id == uid).one()

        db.session.delete(movie_data)
        db.session.commit()

        return 'movie_deleted', 204
