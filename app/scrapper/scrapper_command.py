import click
from app.scrapper.scrapper import batch_scraping_by_genre
from app.models.movie import Movie
from flask.cli import with_appcontext

@click.command('scrape')
@click.option('-g','--genre', type=str, required=True)
@click.option('-n', '--page_number', type=int)
@with_appcontext
def scrape_cmd(genre, page_number): 
  movies = batch_scraping_by_genre(genre,  page_number or 1)

  for res_scraping in movies:
    new_movie = Movie(title=res_scraping["title"])
    new_movie.rating = res_scraping["rating"]
    new_movie.reviews = res_scraping["review"]
    new_movie.summary = res_scraping["summary"]
    new_movie.writers = res_scraping["writers"]
    new_movie.directors = res_scraping["directors"]
    new_movie.genre = res_scraping["genre"]
    new_movie.stars = res_scraping["stars"]
    new_movie.year = res_scraping["year"]
    new_movie.casts = res_scraping["cast"]
    new_movie.img = res_scraping["img"]
    new_movie.meta.id = res_scraping["id"]
    new_movie.save()
    print(new_movie)