from elasticsearch_dsl import (
  InnerDoc, Text
)
from .index import normalization_analyzer

class Cast(InnerDoc):
  name = Text(analyzer = normalization_analyzer)
  character = Text(analyzer = normalization_analyzer)
  img = Text(analyzer = None)
