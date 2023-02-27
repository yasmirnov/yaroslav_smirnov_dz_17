from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


api = Api(app)

api.add_namespace(movie_ns)
api.add_namespace(director_ns)
api.add_namespace(genre_ns)

if __name__ == '__main__':
    app.run(debug=True)
