import os
import django
import requests
import sqlite3

from criticscorner.settings import SECRET_KEY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'criticscorner.settings')
django.setup()
from django.db import connection


def write_to_db(data, table_name):
    conn = sqlite3.connect("db.sqlite3")  # Define the data you want to insert

    # Build the SQL query
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    values = list(data.values())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query, values)
        connection.close()


def fetch_movies_from_api():
    url = "https://imdb-top-100-movies.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    print('RESPONSE:', response)
    movies_list = response.json()
    print('LISTA DE MOVIES:', movies_list)
    print('Numero de filmes:', len(movies_list))

    for movie in movies_list:
        print('Movie:', movie)
        api_id = movie.get('id')
        print("Adicionar o filme com id " + api_id)

        fetch_movies_details_and_populate_database(api_id)


def fetch_movies_details_and_populate_database(api_id):
    url = f"https://imdb-top-100-movies.p.rapidapi.com/{api_id}"

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
    }

    params = {"id": api_id}
    response = requests.get(url, headers=headers, params=params)
    movie = response.json()

    print("\t\tFilme com o nome " + movie.get("title")
          + "\n\t\t do ano " + str(movie.get("year"))
          + "\n\t\t com o poster " + movie.get("image")
          + "\n\t\t com a plot " + movie.get("description")
          + "\n\t\t com os diretores " + str(movie.get("director"))
          + "\n\t\t com os autores " + str(movie.get("writers"))
          + "\n\t\t com os generos " + str(movie.get("genre")))

    data = {
        "imdb_id": movie.get("imdbid"),
        "title": movie.get("title"),
        "year": int(movie.get("year")),
        "poster_url": str(movie.get("image")),
        "plot": movie.get("description"),
        "director": str(movie.get("director")),
        "writer": str(movie.get("writers")),
        "genres": str(movie.get("genre"))
    }

    write_to_db(data, "review_movie")


fetch_movies_from_api()
