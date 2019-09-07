from flask import (
  Blueprint, render_template, request
)
from app.models.movie import Movie
from app.models.queries import get_all_genre
homepage_blueprint = Blueprint('homepage', __name__, url_prefix='/')

@homepage_blueprint.route('/', methods=['GET'])
def render_homepage():
  is_search = False

  query = request.args.get('search', None)
  genre = request.args.get('genre', '')
  min_rate = request.args.get('min-rate', '')
  max_rate = request.args.get('max-rate', '')
  if query:
    is_search = True
    print(query, genre, min_rate, max_rate)

  search = Movie.search()
  results = search.execute()
  all_genre = get_all_genre()
  return render_template('homepage/home.html', movies = results, genres = all_genre, is_search = is_search )
