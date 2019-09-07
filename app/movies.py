from flask import (
  Blueprint, render_template, request
)

movies_blueprint = Blueprint('movies', __name__, url_prefix='/movies')

@movies_blueprint.route('/<id>', methods=['GET'])
def render_movie(id):
  return render_template('movies/detail.html')
