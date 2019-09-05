from elasticsearch_dsl import (
  InnerDoc, Text, Float
)
from .index import normalization_analyzer

class Review(InnerDoc):
  username = Text(analyzer = normalization_analyzer)
  title = Text(analyzer = normalization_analyzer)
  content = Text(analyzer = normalization_analyzer)
