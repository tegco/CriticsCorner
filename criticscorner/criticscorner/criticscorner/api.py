import requests

from criticscorner.criticscorner.settings import SECRET_KEY


# from .models import Movie

def fetch_movies_from_api():
    url = "https://online-movie-database.p.rapidapi.com/title/get-top-rated-movies"

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    movie_list = response.json()
    print(len(movie_list))

    for movie in movie_list:
        print(movie['id'])

    return response


# def populate_database():


fetch_movies_from_api()
