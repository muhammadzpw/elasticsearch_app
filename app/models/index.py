import os
from elasticsearch_dsl import (
  Index, tokenizer, analyzer
)
from pprint import pprint

movie_index: Index = Index(os.environ.get('ES_INDEX', 'moovie'))

movie_index.settings(
  number_of_shards=5,
  number_of_replicas=1
)

completion_analyzer = analyzer(
  'completion_analyzer',
  tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
  filter=['lowercase']
)

normalization_analyzer = analyzer(
  'normalization_analyzer',
  tokenizer="standard",
  filter=["standard", "lowercase", "stop", "snowball"],
  char_filter=["html_strip"]
)

movie_index.analyzer(normalization_analyzer)

def init_index():
  if not movie_index.exists():
    movie_index.create()
    
def destroy_index():
  if movie_index.exists():
    movie_index.delete(ignore=404)
