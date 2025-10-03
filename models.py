from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# FROM APP.PY
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

#here happens the magic - 1 user plural movies
    movies = db.relationship(
        "Movie",
        backref="user",
        cascade="all, delete-orphan",
        lazy=True,
    )


    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r}>"

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(10))
    imdb_id = db.Column(db.String(20))
    poster_url = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Movie id={self.id} title={self.title!r} user_id={self.user_id}>"