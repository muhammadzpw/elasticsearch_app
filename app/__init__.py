#pylint: disable=unused-variable
import os
from flask import Flask, render_template
from . import models

def create_app(test_config=None):
  app = Flask(__name__)
  
  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)

  try:
      os.makedirs(app.instance_path)
  except OSError:
      pass

  from . import homepage
  app.register_blueprint(homepage.homepage_blueprint)

  from . import movies
  app.register_blueprint(movies.movies_blueprint)

  from . import search
  app.register_blueprint(search.search_blueprint)

  @app.errorhandler(404)
  def page_not_found(error):
    return render_template('404.html'), 404

  models.init_app(app)

  return app
