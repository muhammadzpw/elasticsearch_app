from flask import (
  Blueprint, render_template, request, jsonify
)
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from app.models.movie import Movie
from app.scrapper.scrapper import single_scraping

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')

@movies_blueprint.route('/', methods=['GET'])
def render_movies():
  return render_template('movies/detail.html')

@movies_blueprint.route('/add', methods=['GET', 'POST'])
def render_add_movies():
  if request.method == 'GET':
    return render_template('movies/add.html')

  elif request.method == 'POST':
    movies_url = request.form['moviesUrl']
    movies_id = movies_url.split('/')[4]
    movie_data = Movie.get(id=movies_id, ignore=404)
    print('movie data', movie_data)
    if movie_data is None:
      print('id not found, start scraping')
      res_scraping = single_scraping(movies_url)
      new_movie = Movie(title=res_scraping["title"])
      new_movie.rating = res_scraping["rating"]
      new_movie.reviews = res_scraping["review"]
      new_movie.summary = res_scraping["summary"]
      new_movie.writers = res_scraping["writers"]
      new_movie.directors = res_scraping["directors"]
      new_movie.genre = res_scraping["genre"]
      new_movie.stars = res_scraping["stars"]
      new_movie.year = res_scraping["year"]
      new_movie.casts = res_scraping["cast"]
      new_movie.img = res_scraping["img"]
      new_movie.meta.id = movies_id
      new_movie.save()

    es = Elasticsearch()
    res = es.get(index='moovie', doc_type='_doc', id=movies_id)
    return jsonify(res['_source'])
