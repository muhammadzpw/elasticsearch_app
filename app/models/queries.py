from elasticsearch_dsl import A
from app.models.movie import Movie
from pprint import pprint

search = Movie.search()

def get_all_genre():
  genre_agg = A('terms', field = 'genre.raw')
  search.aggs.bucket('genre_terms', genre_agg)
  result = search.execute()
  # pprint(result.aggregations['genre_terms']['buckets'])
  return result.aggregations['genre_terms']['buckets']
