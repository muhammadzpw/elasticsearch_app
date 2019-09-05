from elasticsearch_dsl import (
  Document, analyzer, tokenizer, Text, Completion,
  Keyword, Date, Float, Integer, Nested
)
from .index import (
  movie_index, completion_analyzer, normalization_analyzer
)
from .cast import Cast
from .review import Review
from itertools import permutations

@movie_index.document
class Movie(Document):
  img = Text()
  title = Text(analyzer = normalization_analyzer)
  year = Integer()
  summary = Text(analyzer = normalization_analyzer)
  rating = Float()
  writers = Text(
    analyzer = normalization_analyzer,
    fields={'raw': Keyword()}
  )
  genre = Text(
    analyzer = normalization_analyzer,
    fields={'raw': Keyword()}
  )
  directors = Text(
    analyzer = normalization_analyzer,
    fields={'raw': Keyword()}
  )
  stars = Text(
    analyzer = normalization_analyzer,
    fields={'raw': Keyword()}
  )

  suggest = Completion(analyzer=completion_analyzer)

  casts = Nested(Cast)
  reviews = Nested(Review)

  def clean(self):
    self.suggest = {
      'input': [' '.join(p) for p in permutations(self.title.split())],
    }

def init():
  Movie.init()
  