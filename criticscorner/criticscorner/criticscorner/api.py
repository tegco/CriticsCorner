import requests

from criticscorner.criticscorner.settings import SECRET_KEY
from criticscorner.review.models import Movie


# from .models import Movie

def fetch_movies_from_api():
    url = "https://online-movie-database.p.rapidapi.com/title/get-top-rated-movies"

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    movies_list = response.json()
    print(len(movies_list))

    for movie in movies_list:
        print(movie['id'])
        imdb_id = movie["id"]
        movie_exists = Movie.objects.filter(imdb_id=imdb_id).first()
        if movie_exists:
            continue

        title = movie["title"]
        fetch_movies_details_and_populate_database(title, imdb_id)


def fetch_movies_details_and_populate_database(title, imdb_id):
    url = "https://online-movie-database.p.rapidapi.com/title/find"

    headers = {
        "X-RapidAPI-Key": SECRET_KEY,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    params = {"q": title}
    response_find = requests.get(url, headers=headers, params=params)
    movie = response_find.json()

    if not movie:
        return

        # Verify that the found movie has the same imdb_id
    if movie[0]['id'] != imdb_id:
        return

        # Get the movie's details by imdb_id
    params_details = {"tconst": imdb_id}
    response_details = requests.get(url, headers=headers, params=params_details)
    movie_data = response_details.json()

    if "error" not in movie_data:
        movie = Movie(
            imdb_id=imdb_id,
            title=movie_data["title"],
            year=int(movie_data["release_date"][:4]),
            poster_url=movie_data["poster"],
            plot=movie_data.get("plot", ""),
            director=movie_data.get("directors", [""])[0],
            writer=movie_data.get("writers", [""])[0],
            duration=movie_data.get("runtime", 0),
            genres=", ".join(movie_data.get("genres", [])),

        )
        movie.save()
        print(movie.imdb_id, movie.title, movie.year, movie.poster_url, movie.plot,
              movie.director, movie.writer, movie.duration, movie.genres)


fetch_movies_from_api()
