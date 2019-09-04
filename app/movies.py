from flask import (
  Blueprint, render_template, request
)

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')

@movies_blueprint.route('/', methods=['GET'])
def render_movies():
  return render_template('movies/detail.html')
