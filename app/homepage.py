from flask import (
  Blueprint, render_template, request
)

homepage_blueprint = Blueprint('homepage', __name__, url_prefix='/')

@homepage_blueprint.route('/', methods=['GET'])
def render_homepage():
  return render_template('homepage/home.html')
