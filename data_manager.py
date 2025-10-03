from django.contrib.sessions.backends import db
from models import db, User, Movie


class Datamanager():

  def create_user(self, name: str) -> User:
    user = User(name=name.strip())
    db.session.add(user)
    db.session.commit()
    return user

  def get_users(self):
    return User.query.order_by(User.name.asc()).all()


# following all function, belonging to "MOVIES"
  def get_movies(self, user_id: int):
    return Movie.query.filter_by(user_id=user_id).order_by(Movie.title.asc()).all()

  def add_movie(self, user_id: int) -> Movie:
    if isinstance(movie, Movie):
      m = movie
      m.user_id = user_id
    else:
      m = Movie(
        user_id=user_id,
        title=str(movie.get("title", "")).strip(),
        year=movie.get("year"),
        imdb_id=movie.get("imdb_id"),
        poster_url=movie.get("poster_url"),
      )
    if not m.title:
      raise ValueError("Movie title may not be empty...")
    db.session.add(m)
    db.session.commit()
    return m

  def update_movie(self, movie_id: int, new_title: str) -> Movie:
    m: Optional[Movie] = Movie.query.get(movie_id)
    if not m:
      raise ValueError(f"Movie {movie_id} does not exist.")
    m.title = new_title.strip()
    db.session.commit()
    return m

  def delete_movie(self, movie_id: int) -> None:
    m: Optional[Movie] = Movie.query.get(movie_id)
    if not m:
      # idempotent: still ok
      return
    db.session.delete(m)
    db.session.commit()



