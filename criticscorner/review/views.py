from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


def index(request):
    movies = Movie.objects.all()
    return render(request, 'review/list_movies.html', {'movies': movies})


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('user')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)
        rv = Reviewer(user=user)
        rv.save()

        return HttpResponseRedirect(reverse('review:loginview'))  # <-- Ver se isto está bem
    else:
        return render(request, 'review/registeruser.html')  # <-- Mudar nome do template


def loginview(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('review:index'))
        else:
            return render(request, 'review/login.html', {'error_message': "Invalid username or password!"}, )
    else:
        return render(request, 'review/login.html')


@login_required(login_url='review:loginview')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('review:index'))


@login_required(login_url='review:loginview')
def details(request, movie_id):
    # Ver se o objeto movie tem acesso a todas as reviews
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    try:
        watchlists = Watchlist.objects.filter(reviewer=request.user.reviewer.user_id)
    except Watchlist.DoesNotExist:
        watchlists = None

    context = {
        'movie': movie,
        'reviews': reviews,
        'watchlists': watchlists
    }
    return render(request, 'review/details.html', context)


@login_required(login_url='review:loginview')
def review_movie(request, movie_id):
    # # Ver se o objeto movie tem acesso a todas as reviews
    movie = get_object_or_404(Movie, pk=movie_id)
    # reviews = Review.objects.filter(movie=movie)
    # try:
    #     watchlists = Watchlist.objects.filter(reviewer=request.user.reviewer.user_id)
    # except Watchlist.DoesNotExist:
    #     watchlists = None
    #
    # context = {
    #     'movie': movie,
    #     'reviews': reviews,
    #     'watchlists': watchlists
    # }

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('review:details', args=(movie_id,)))

    try:
        rating = request.POST['rating']  # Rating é obrigatório para todas as reviews
        comment = request.POST['comment']
    except KeyError:
        messages.error(request=request, message="Fields missing")
        return render(request, 'review/details.html', {'movie': movie, 'error_message': "Fields missing."})

    if rating:
        if not comment or comment == "":
            comment = None  # <-- Ver se isto é transformado para 'null' na base de dados

        new_review = Review(rating=rating,
                            comment=comment,
                            likes_count=0,
                            created_at=timezone.now(),
                            movie_id=movie_id,
                            reviewer_id=request.user.reviewer.user_id)
        new_review.save()

        messages.success(request=request, message="Review successfully added!")
        return HttpResponseRedirect(reverse('review:details', args=(movie_id,)))

    messages.error(request=request, message="Review does not have a rating.")
    return HttpResponseRedirect(reverse('review:details', args=(movie_id,)))


@permission_required('auth.delete_movie')
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.delete()
    return HttpResponseRedirect(reverse('review:index'))


@api_view(['GET'])
def list_movies(request):
    movies = Movie.objects.all()
    movie_serializer = MovieSerializer(movies, context={'request': request}, many=True)
    return Response(movie_serializer.data)


@login_required(login_url='review:loginview')
def add_to_watchlist(request, movie_id):
    if request.method == 'POST':
        watchlist_id = request.POST.get('watchlist_id')
        watchlist = get_object_or_404(Watchlist, pk=watchlist_id)
        movie = Movie.objects.get(pk=movie_id)

        if watchlist.movies.filter(pk=movie_id).exists():
            messages.warning(request, 'Movie is already in the watchlist.')
        else:
            watchlist.movies.add(movie)
            messages.success(request, 'Movie successfully added!')
    return HttpResponseRedirect(reverse('review:review_movie', args=(movie.id,)))


@login_required(login_url='review:loginview')
def delete_from_watchlist(request, movie_id, watchlist_id):
    if request.method == 'POST':
        watchlist_id = request.POST.get('watchlist_id')
        watchlist = get_object_or_404(Watchlist, pk=watchlist_id)
        movie = Movie.objects.get(pk=movie_id)

        if watchlist.movies.filter(pk=movie_id).exists():
            watchlist.movies.remove(movie)
            messages.success(request, 'Movie deleted from the watchlist.')
        else:
            messages.error(request, 'Couldn´t delete movie from watchlist!')
    return HttpResponseRedirect(reverse('review:display_watchlist'))


@login_required(login_url='review:loginview')
def display_watchlist(request):
    watchlists = Watchlist.objects.filter(reviewer_id=request.user.reviewer.user_id)
    movies_in_watchlists = []
    for watchlist in watchlists:
        movies = watchlist.movies.all()
        movies_in_watchlists.append((watchlist, movies))

    return render(request, 'review/watchlist.html', {'movies_in_watchlists': movies_in_watchlists})


@login_required(login_url='review:loginview')
def like_movie(request, review_id):
    review = Review.objects.get(pk=review_id)
    reviewer_liking = request.user.reviewer
    current_likes = review.likes_count

    liked = Like.objects.filter(reviewer=reviewer_liking, review=review).count()

    if not liked:
        like = Like.objects.create(reviewer=reviewer_liking, review=review, created_at=timezone.now())
        current_likes = current_likes + 1
    review.likes_count = current_likes
    review.save()
    return HttpResponseRedirect(reverse('review:review_movie', args=(review.movie.id,)))


# @api_view(['GET'])
# def movie_detail(request, movie_id):
#     try:
#         movie = Movie.objects.get(pk=movie_id)
#     except Movie.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
def send_to_front_end(request):
    return HttpResponseRedirect('http://localhost:3000/')  # Redireciona ao react
