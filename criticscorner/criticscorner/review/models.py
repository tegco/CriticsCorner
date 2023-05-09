from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField("Review", through='Like',
                                           related_name='liked_by')  # significa que o modelo Like é usado p/ gerir a relação Reviewer-Review
    reviews = models.ManyToManyField("Review", through='Rating', related_name='rated_by')
    profile_picture = models.CharField(max_length=100)


class Movie(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    plot = models.TextField()
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    poster_url = models.URLField()
    genres = models.CharField(max_length=100)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    watchlists = models.ManyToManyField("Watchlist")

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.imdb_id
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews_received")
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name="reviews_given")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True, null=True,
                               max_length=450)  # Este campo não é obrigatório, se não for preenchido é guardado como " "
    likes_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(Reviewer, related_name="liked_reviews")
    created_at = models.DateTimeField(
        auto_now_add=True)  # timestamp para a publicação da review -> não pode ser modificado

    # updated_at = models.DateTimeField(auto_now=True) #quando a review é alterada, pode-se dar update a esta data

    class Meta:  # Um reviewer só pode deixar uma review em cada filme
        unique_together = ("reviewer", "movie")


class Like(models.Model):
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name="likes_given")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # Um reviewer só pode deixar um gosto em cada review
        unique_together = ("reviewer", "review")


class Rating(models.Model):
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name="ratings_given")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="ratings_received")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings_received")

    class Meta:  # Um reviewer só pode deixar um rating em cada review
        unique_together = ("reviewer", "movie")


class Watchlist(models.Model):
    name = models.CharField(max_length=100)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    movies = models.ManyToManyField("Movie")
