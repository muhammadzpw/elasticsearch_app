from elasticsearch_dsl import connections
import os
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext
from pprint import pprint
from . import index, movie

APP_CONNECTION_ALIAS = 'default'

@click.command('make-schema')
@with_appcontext
def init_schema_command():
  schema_init()
  click.echo('Schema initialized.')

@click.command('destroy-schema')
@with_appcontext
def destroy_schema_command():
  index.destroy_index()
  click.echo('Schema destroyed.')

@click.command('reset-schema')
@with_appcontext
def reset_schema_command():
  index.destroy_index()
  index.init_index()
  click.echo('Schema destroyed.')

def schema_init():
  index.init_index()

def init_connections(app: Flask):
  conn = connections.create_connection(APP_CONNECTION_ALIAS, hosts=[{
    'host': os.environ.get('ES_HOST', 'localhost'),
    'port': os.environ.get('ES_PORT', 9200)
  }], timeout=60)
  pprint(conn.info())

def init_app(app: Flask):
  app.cli.add_command(init_schema_command)
  app.cli.add_command(destroy_schema_command)
  app.cli.add_command(reset_schema_command)
  init_connections(app)
  schema_init()

