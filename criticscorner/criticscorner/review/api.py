import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "criticscorner.criticscorner.criticscorner.settings")

django.setup()

import requests
from django.conf import settings

from criticscorner.criticscorner.criticscorner.settings import BASE_DIR, SECRET_KEY


settings.configure(
    INSTALLED_APPS=['review.apps.ReviewConfig', 'django.contrib.admin', 'django.contrib.auth',
                    'django.contrib.contenttypes', 'django.contrib.sessions',
                    'django.contrib.messages', 'django.contrib.staticfiles', ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "criticscorner.settings")


def fetch_movies_from_api():

    url = "https://online-movie-database.p.rapidapi.com/title/get-top-rated-movies"

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    movies_list = response.json()
    print('Numero de filmes:', len(movies_list))

    for movie in movies_list:
        imdb_id = movie['id'].split('/')[2]
        print("Adicionar o filme com id " + imdb_id)
        fetch_movies_details_and_populate_database(imdb_id)


def fetch_movies_details_and_populate_database(imdb_id):
    url = "https://online-movie-database.p.rapidapi.com/title/find"

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    params = {"q": imdb_id}
    response = requests.get(url, headers=headers, params=params)
    movie = response.json().get("results")[0]

    top_crew = fetch_top_crew(imdb_id)
    print("\t\tFilme com o nome " + movie.get("title")
          + "\n\t\t do ano " + str(movie.get("year"))
          + "\n\t\t com o poster " + movie.get("image").get("url")
          + "\n\t\t com duração " + str(movie.get("runningTimeInMinutes"))
          + "\n\t\t com a plot " + fetch_plot(imdb_id)
          + "\n\t\t com os diretores " + str(top_crew[0])
          + "\n\t\t com os autores " + str(top_crew[1])
          + "\n\t\t com os generos " + str(fetch_genres(imdb_id)))

    from criticscorner.criticscorner.review.models import Movie
    movie = Movie(
        imdb_id=imdb_id,
        title= movie.get("title"),
        year= int(movie.get("year")),
        poster_url= movie.get("image").get("url"),
        plot= fetch_plot(imdb_id),
        director=str(top_crew[0]),
        writer=str(top_crew[1]),
        duration= movie.get("runningTimeInMinutes"),
        genres=str(fetch_genres(imdb_id))
    )
    movie.save()
    print(f"Saved movie {movie.title} to the database")

def fetch_plot(imdb_id):
    url = "https://online-movie-database.p.rapidapi.com/title/get-plots"

    querystring = {"tconst": imdb_id}

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json().get("plots")[0].get("text")



def fetch_top_crew(imdb_id):

    url = "https://online-movie-database.p.rapidapi.com/title/get-top-crew"

    querystring = {"tconst": imdb_id}

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)


    dir_array = []
    for director in response.json().get("directors"):
        dir_array.append(director.get("name"))

    wri_array = []
    for writer in response.json().get("writers"):
        wri_array.append(writer.get("name"))

    return [dir_array, wri_array]


def fetch_genres(imdb_id):
    url = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"

    querystring = {"tconst": imdb_id}

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json().get("genres")

fetch_movies_from_api()
