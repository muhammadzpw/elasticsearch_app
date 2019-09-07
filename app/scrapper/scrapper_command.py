import click
from app.scrapper.scrapper import batch_scraping_by_genre

@click.command('scrape')
@click.option('-g','--genre', type=string, required=True)
@click.option('-n', '--page_number', type=int)
@with_appcontext
def seeds_cmd(genre, page_number): 
  movies = batch_scraping_by_genre(genre,  page_number or 1)

  for movie in movies:
    
    print(movie)