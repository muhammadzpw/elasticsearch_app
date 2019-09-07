from flask import (
  Blueprint, render_template, request
)
from elasticsearch_dsl import Q
from app.models.movie import Movie
from app.models.queries import get_all_genre
homepage_blueprint = Blueprint('homepage', __name__, url_prefix='/')

@homepage_blueprint.route('/', methods=['GET'])
def render_homepage():
  is_search = False
  search = Movie.search()
  query = request.args.get('search', None)
  genre = request.args.get('genre', [])
  min_rate = request.args.get('min-rate', '')
  max_rate = request.args.get('max-rate', '')
  if request.args:
    is_search = True
    q = Q('bool',
      must=[Q('match', title=query)],
      should=[Q('match', summary=query)]
    )
    search = search.query("match", q)
    print(query, genre, min_rate, max_rate)
    search = search.filter('terms', genre=genre)

  results = search.execute()
  all_genre = get_all_genre()
  return render_template('homepage/home.html', movies = results, genres = all_genre, is_search = is_search )
