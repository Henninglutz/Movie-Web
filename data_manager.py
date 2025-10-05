from __future__ import annotations
from django.contrib.sessions.backends import db

import os
from typing import Any, Dict, Optional, Union, List
import requests
from dotenv import load_dotenv
from models import db, User, Movie

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")



class Datamanager():
#USER
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

#getting the data form IMDB
  def add_movie(self, user_id: int, movie: dict):
    title = movie.get("title", "").strip()
    year = movie.get("year")
    if not title:
        raise ValueError("Movie title may not be empty")

    details = self.fetch_movie_from_omdb(title, year)

    m = Movie(
      user_id=user_id,
      title=details.get("title", title) if isinstance(details, dict) else title,
      year=details.get("year") if isinstance(details, dict) and details.get("year") is not None else year,
      imdb_id=details.get("imdb_id") if isinstance(details, dict) else None,
      poster_url=details.get("poster_url") if isinstance(details, dict) else None,
    )

    db.session.add(m)
    db.session.commit()
    return m

    db.session.add(m)
    db.session.commit()
    return m

  def update_movie(self, movie_id: int, new_title: str) -> Movie:
    m = Movie.query.get(movie_id)
    if not m:
      raise ValueError(f"Movie {movie_id} does not exist.")
    m.title = new_title.strip()
    db.session.commit()
    return m


  def delete_movie(self, movie_id: int) -> None:
    m = Movie.query.get(movie_id)
    if not m:
      return
    db.session.delete(m)
    db.session.commit()



#API calling
  def fetch_movie_from_omdb(self, title, year=None):
    import os, requests
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        raise ValueError("OMDB_API_KEY not found in .env file")

    params = {"apikey": api_key, "t": title}
    if year:
        params["y"] = str(year)

    resp = requests.get("https://www.omdbapi.com/", params=params, timeout=10)
    resp.raise_for_status()
    raw = resp.json()

    if raw.get("Response") != "True":
        return {}

    yr = raw.get("Year")
    year_int = int(yr) if isinstance(yr, str) and yr.isdigit() else None

    poster = raw.get("Poster")
    if poster in (None, "N/A"):
        poster = None

    return {
        "title": raw.get("Title") or title,
        "year": year_int,
        "imdb_id": raw.get("imdbID"),
        "poster_url": poster,
    }
