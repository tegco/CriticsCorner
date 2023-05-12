from django.urls import include, path
from . import views

app_name = 'review'

urlpatterns = [
    # Views the templates de Django
    path("", views.index, name="index"),
    path('register', views.register_user, name='register_user'),
    path('logout', views.logoutview, name='logoutview'),
    path('login', views.loginview, name='loginview'),
    path('watchlist/add/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlists', views.display_watchlist, name='display_watchlist'),
    #path('<int:movie_id>', views.details, name='details'),
    # O admin pode apagar um movie
    path('<int:movie_id>/delete_movie', views.delete_movie, name='delete_movie'),
    # Para fazer POST de uma review
    path('<int:movie_id>', views.review_movie, name='review_movie'),
    #Para dar like a uma review
    path('<int:review_id>/like', views.like_movie, name='like_movie'),

    # Views de react
    # Para listar todos os  movies (página principal)
    path('api/movies/', views.list_movies, name='list_movies'),
]
