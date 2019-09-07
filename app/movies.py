from flask import (
  Blueprint, render_template, request, jsonify, redirect, url_for
)
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from app.models.movie import Movie
from app.scrapper.scrapper import single_scraping

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')

@movies_blueprint.route('/<id>', methods=['GET'])
def render_movie(id):
  movie = Movie.get(id=id, ignore=404)
  return render_template('movies/detail.html', movie = movie)

@movies_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
def render_edit_movie(id):
  movie = Movie.get(id=id, ignore=404)
  if request.method == 'POST':
    movie.title = request.form['title']
    movie.summary = request.form['summary']
    movie.save()
    return redirect(url_for('movies.render_movie', id = movie.meta.id))
  return render_template('movies/detail.html', movie = movie, is_edit=True)

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
