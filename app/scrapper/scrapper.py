#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:09:10 2019

@author: fhabibie
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import json
import re

BASE_URL = 'https://www.imdb.com'

def single_scraping(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    movie_title = soup.find('div', {'class' : 'title_wrapper'}).find('h1').text
    movie_img = soup.find('div', {'class': 'poster'}).find('img').get('src')
    movie_year = soup.find('span', {'id' : 'titleYear'}).find('a').text
    movie_summary = soup.find('div', {'class' : 'summary_text'}).text
    directors, writers, stars = soup.find_all('div', {'class' : 'credit_summary_item'})
    movie_rating = soup.find('span', {'itemprop' : 'ratingValue'}).text
    
    tmp_director, tmp_writer, tmp_star = [], [], []
    for credit in directors.find_all('a', href= re.compile('name')):
        tmp_director.append(credit.text)
    for credit in writers.find_all('a', href= re.compile('name')):
        tmp_writer.append(credit.text)
    for credit in stars.find_all('a', href= re.compile('name')):
        tmp_star.append(credit.text)

    print('\n')

    storyline = soup.find('div', {'id' : 'titleStoryLine' })
    
    story_items = storyline.find_all('div', {'class' : 'see-more inline canwrap'})
    
    tmp_gen = []
    for item in story_items:
        genres = item.find_all('a', href = re.compile('genres'))
        for gen in genres:
            tmp_gen.append(gen.text.strip())
                
    casts = soup.find('table', {'class' : 'cast_list'}).find_all('tr')
    print('movie title : ', movie_title)
    
    movie_id = url.split('/')[4]
    print('movie id \t: ', movie_id)
    tmp_casts = get_all_casts(movie_id)
    tmp_reviews = get_all_reviews(movie_id)
    single_result = {
            "title" : movie_title,
            "link" : url,
            "img" : movie_img,
            "summary" : re.sub(r"^\s+", "", movie_summary),
            "directors" : tmp_director,
            "writers" : tmp_writer,
            "stars" : tmp_star,
            "year" : movie_year,
            "rating" : float(movie_rating),
            "genre" : tmp_gen,
            "cast" :tmp_casts,
            "review" : tmp_reviews
            }
    return single_result

def get_all_casts(movie_id):
    credit_link = BASE_URL + '/title/' + movie_id + '/fullcredits'
    credit_page = urlopen(credit_link)
    credit_soup = BeautifulSoup(credit_page, "html.parser")
    
    print('casts url \t: ', credit_link)
    casts_table = credit_soup.find('table', {'class': 'cast_list'}).find_all('tr', {'class' : 'odd', 'class': 'even'})
    print('total \t: ' , len(casts_table))
    tmp_casts = []
    if len(casts_table) > 1:
#        for i in range(1, len(casts_table)):
        i = 1
        while i < 16 and i < len(casts_table):
            img, name, _, character = casts_table[i].find_all('td', )
            img = img.find('img').get('src')
            name = name.text.strip()
            character = character.text.strip()
            tmp_casts.append( {'img' : img,
                        "name" : name,
                        "character" : character})
            i+= 1
    return tmp_casts
        

def get_all_reviews(movie_id):
    review_link = BASE_URL + '/title/'+movie_id+'/reviews?sort=totalVotes&dir=desc'
    review_page = urlopen(review_link)
    review_soup = BeautifulSoup(review_page, "html.parser")
    
    print('review url \t: ', review_link)
    review_lists = review_soup.find_all('div', {'class': 'lister-item-content'})
    print('total \t: ', len(review_lists))
    tmp_reviews = []
    if(len(tmp_reviews) > 0):
        i = 0
        while i < 5 and i < len(tmp_reviews):
            title = review_lists[i].find('a', {'class': 'title'}).text
            username = review_lists[i].find('span', {'class': 'display-name-link'}).text
            content = review_lists[i].find('div', {'class': 'text show-more__control'}).text
            tmp_reviews.append({
                    "username" : username.strip(),
                    "title" : title.strip(),
                    "content" : content.strip()
                    })
            i += 1
    return tmp_reviews

def batch_scraping_by_genre(genre, num_pages):
    start_pages = 0
    for i in range(0, num_pages):
        movies_url = BASE_URL + '/search/title/?title_type=feature&genres=' + str(genre) + '&user_rating=1.0,10.0&start=' + str(start_pages)
        movies_page = urlopen(movies_url)
        movies_soup = BeautifulSoup(movies_page, "html.parser")
        start_pages += 50
        
        movie_list = movies_soup.find_all('h3', class_='lister-item-header')
        
        result = []
        for movie in movie_list:
            movie_link = movie.find('a').get('href')
            single_res = single_scraping(BASE_URL + movie_link)
            result.append(single_res)
        return result

def batch_scraping(urls):
    movie_url = urls + '&title_type=feature&user_rating=1.0,10.0'
    movie_page = urlopen(movie_url)
    movies_soup = BeautifulSoup(movie_page, "html.parser")
    
    movie_list = movies_soup.find_all('h3', class_='lister-item-header')
    
    result = []
    for movie in movie_list:
        movie_link = movie.find('a').get('href')
        single_res = single_scraping(BASE_URL + movie_link)
        result.append(single_res)
    
    return result

#def main():
#    sample run
#    1. Batch scraping
#    movie_urls = 'https://www.imdb.com/search/title/?title_type=feature&start=51&ref_=adv_nxt&start=100'
#    batch = batch_scraping(movie_urls)
#    batch_json = json.dumps(batch)
#    with open('samples/batch-'+ str(datetime.datetime.now()) +'.txt', 'w') as f:
#        f.write(batch_json)

#   2. Batch by genre
#    genre = 'Comedy'
#    num_pages = 1
#    batch_genre = batch_scraping_by_genre(genre, num_pages)
#    batch_genre_json = json.dumps(batch_genre)
#    with open('samples/genres-' + str(datetime.datetime.now()) + '.txt', 'w') as f:
#        f.write(batch_genre_json)
#        
#    3. Single movie page
#    urls = 'https://www.imdb.com/title/tt8009314/?ref_=adv_li_tt'        
#    single = single_scraping(urls)
#    json_string = json.dumps(single)
#    with open ('./samples/single-' + str(datetime.datetime.now()) + '.txt', 'w') as f:
#        f.write(json_string)
        
#if __name__ == '__main__':
#    main()
        
#%%    
    