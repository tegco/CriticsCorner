from django.urls import include, path
from . import views

app_name = 'review'

urlpatterns = [
    # Views the templates de Django
    path("", views.index, name="index"),
    path('register', views.register_user, name='register_user'),
    path('logout', views.logoutview, name='logoutview'),
    path('login', views.loginview, name='loginview'),
    path('watchlist/create/', views.create_watchlist, name='create_watchlist'),
    path('watchlist/<int:watchlist_id>/delete/', views.delete_watchlist, name='delete_watchlist'),
    path('watchlist/add/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/<int:watchlist_id>/delete/<int:movie_id>/', views.delete_from_watchlist, name='delete_from_watchlist'),
    path('watchlists', views.display_watchlist, name='display_watchlist'),
    path('<int:movie_id>', views.details, name='details'),
    # O admin pode apagar um movie
    path('<int:movie_id>/delete_movie', views.delete_movie, name='delete_movie'),
    # Para fazer POST de uma review
    path('<int:movie_id>/review', views.review_movie, name='review_movie'),
    #Para dar like a uma review
    path('<int:review_id>/like', views.like_movie, name='like_movie'),
    #Para apagar uma review
    path('<int:review_id>/delete_review', views.delete_review, name='delete_review'),
    path('topRated', views.send_to_front_end, name="top_rated"),
    # Views de react
    # Para listar todos os  movies (página principal)
    path('api/movies', views.list_movies, name='list_movies'),
]
