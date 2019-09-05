from elasticsearch_dsl import (
  Document, analyzer, tokenizer, Text, Completion,
  Keyword, Date, Float, Integer, Nested
)
from .index import (
  movie_index, completion_analyzer, normalization_analyzer
)
from .cast import Cast

@movie_index.document
class Movie(Document):
  img = Text(analyzer=None)
  title = Text(analyzer = normalization_analyzer)
  year = Integer()
  summary = Text(analyzer = normalization_analyzer)
  genre = Keyword(analyzer = normalization_analyzer)
  rating = Float()
  writers = Keyword(analyzer = normalization_analyzer)
  directors = Keyword(analyzer = normalization_analyzer)
  stars = Keyword(analyzer = normalization_analyzer)

  suggest = Completion(analyzer=completion_analyzer)

  casts = Nested(Cast)

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
  