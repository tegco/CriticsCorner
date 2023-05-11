from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Reviewer, Movie
from .serializers import *


def index(request):
    # return HttpResponseRedirect('http://localhost:3000/')  # para depois redirecionar ao react
    return render(request, 'review/index.html')


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('user')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)
        rv = Reviewer(user=user)
        rv.save()

        return HttpResponseRedirect(reverse('review:login'))  # <-- Ver se isto está bem
    else:
        return render(request, 'review/registaruser.html')  # <-- Mudar nome do template


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


@login_required(login_url='review:login')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('review:index'))


#@login_required(login_url='review:login')
def details(request, movie_id):
    # Ver se o objeto movie tem acesso a todas as reviews
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'review/details.html', {'movie': movie})


@login_required(login_url='review:login')
def review_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method != 'POST':
        return render(request, 'review/details.html', {'movie': movie})
    try:
        rating = request.POST['rating']  # Rating é obrigatório para todas as reviews
        comment = request.POST['comment']
    except KeyError:
        return render(request, 'review/details.html', {'movie': movie, 'error_message': "Fields missing."})

    if rating:
        if not comment or comment == "":
            comment = None  # <-- Ver se isto é transformado para 'null' na base de dados

        new_review = Review(rating=rating,
                            comment=comment,
                            likes_count=0,
                            created_at=timezone.now(),
                            movie_id=movie_id,
                            reviewer_id=request.user.user_id)
        new_review.save()

        return render(request, 'review/details.html', {'movie': movie, 'success_message': "Review successfully added!"})

    return render(request, 'review/details.html', {'movie': movie, 'error_message': "Review does not have a rating."})


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

# @api_view(['GET'])
# def movie_detail(request, movie_id):
#     try:
#         movie = Movie.objects.get(pk=movie_id)
#     except Movie.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
