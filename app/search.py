from flask import (
  Blueprint, render_template, request
)

search_blueprint = Blueprint('search', __name__, url_prefix='/search')

@search_blueprint.route('/', methods=['GET'])
def render_search():
  return render_template('search/result.html')
