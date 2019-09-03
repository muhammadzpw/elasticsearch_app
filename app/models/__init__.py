from elasticsearch_dsl import connections
import os
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext
from pprint import pprint

APP_CONNECTION_ALIAS = 'default'

@click.command('make-schema')
@with_appcontext
def init_schema_command():
  schema_init()
  click.echo('Schema initialized.')

def schema_init():
  # TODO: Register model here
  print("schemaaaaaaa")
  return

def init_connections(app: Flask):
  conn = connections.create_connection(APP_CONNECTION_ALIAS, hosts=[{
    'host': os.environ.get('ES_HOST', 'localhost'),
    'port': os.environ.get('ES_PORT', 9200)
  }], timeout=60)
  pprint(conn.info())

def teardown_connections(e = None):
  connections.remove_connection(APP_CONNECTION_ALIAS)

def init_app(app: Flask):
  app.cli.add_command(init_schema_command)
  init_connections(app)
  app.teardown_appcontext(teardown_connections)
