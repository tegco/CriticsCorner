from rest_framework import serializers
from .models import Movie, Review


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'imdb_id', 'title', 'year', 'plot', 'director', 'writer', 'poster_url', 'genres', 'avg_rating')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'rating', 'comment', 'likes_count', 'created_at', 'movie_id', 'reviewer_id')


class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'profile_picture', 'user_id')


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'reviewer_id')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'created_at', 'review_id', 'reviewer_id')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'movie_id', 'review_id', 'reviewer_id')
