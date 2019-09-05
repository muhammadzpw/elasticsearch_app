from elasticsearch_dsl import (
  InnerDoc, Text, Float
)
from .index import normalization_analyzer

class Review(InnerDoc):
  name = Text(analyzer = normalization_analyzer)
  review = Text(analyzer = normalization_analyzer)
  rating = Float()
