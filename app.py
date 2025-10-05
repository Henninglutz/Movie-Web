import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import NotNullable
from models import db, User, Movie
from data_manager import Datamanager
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")
basedir = os.path.abspath(os.path.dirname(__file__))

os.makedirs(os.path.join(basedir, "data"), exist_ok=True)
db_path = os.path.join(basedir, "data", "movies.db")

#getting the data via SQALchemy
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["OMDB_API_KEY"] = os.environ.get("OMDB_API_KEY")

#DATABASE and
db.init_app(app)
data_manager = Datamanager()

#create tables
def init_db():
    with app.app_context():
        db.create_all()

init_db()

#ROUTES:
@app.route("/")
def index():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Name may not be empty.", "error")
        return redirect(url_for("index"))
    try:
        user = data_manager.create_user(name)
        flash(f"User '{user.name}' created.", "success")
        return redirect(url_for("get_movies", user_id=user.id))
    except Exception as e:
        flash(f"ups...: {e}", "error")
        return redirect(url_for("index"))


#transfer to movie list of user
@app.get("/users/<int:user_id>")
def show_user(user_id: int):
    User.query.get_or_404(user_id)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies", methods=["GET"], endpoint="get_movies")                             # get movies in data_manager?
def list_movies(user_id: int):                                                             #im template andere name = get_movies()
    user = User.query.get_or_404(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)

@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id: int) -> int:
    title = request.form.get("title", "").strip()
    year = request.form.get("year", "").strip() or None
    if not title:
        flash("Title must be given.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    try:
        data_manager.add_movie(user_id, {"title": title, "year": year})
        flash(f"Movie '{title}' added.", "success")
    except Exception as e:
        flash(f"ups...: {e}", "error")
    return redirect(url_for("get_movies", user_id=user_id))

@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id: int, movie_id: int):
    new_title = request.form.get("new_title", "").strip()
    if not new_title:
        flash("New title, please!", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    try:
        data_manager.update_movie(movie_id, new_title)
        flash("Title updated.", "success")
    except Exception as e:
        flash(f"uppsalla...: {e}", "error")
    return redirect(url_for("get_movies", user_id=user_id))

@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id: int, movie_id: int):
    try:
        data_manager.delete_movie(movie_id)
        flash("Movie deleted.", "success")                          # flash?
    except Exception as e:
        flash(f"Ups...: {e}", "error")
    return redirect(url_for("get_movies", user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


# crate table
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


#"""
# Create the movies table if it does not exist
#with engine.connect() as connection:
#    connection.execute(text("""
#        CREATE TABLE IF NOT EXISTS movies (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            title TEXT UNIQUE NOT NULL,
#            year INTEGER NOT NULL,
#            rating REAL NOT NULL,
#            poster TEXT NOT NULL
#        )
#    """))
#    connection.commit()
