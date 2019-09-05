from elasticsearch_dsl import (
  Document, analyzer, tokenizer, Text, Completion,
  Keyword, Date, Float, Integer, Nested
)
from .index import (
  movie_index, completion_analyzer, normalization_analyzer
)
from .cast import Cast
from .review import Review

@movie_index.document
class Movie(Document):
  img = Text()
  title = Text(analyzer = normalization_analyzer)
  year = Integer()
  summary = Text(analyzer = normalization_analyzer)
  rating = Float()
  writers = Keyword()
  genre = Keyword()
  directors = Keyword()
  stars = Keyword()

  suggest = Completion(analyzer=completion_analyzer)

  casts = Nested(Cast)
  reviews = Nested(Review)

  def clean(self):
    self.suggest = {
      'input': [self.title, self.writers, self.directors, self.stars],
      'weight': self.popularity
    }

  def save(self, ** kwargs):
    save = super().save(** kwargs)
    Movie._index.refresh()
    return save

def init():
  Movie.init()
  