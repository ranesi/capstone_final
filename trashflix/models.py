from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .omdb_api import get_movie_information


class Movie(models.Model):

    title = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    rated = models.CharField(max_length=20, blank=True, null=True)
    released = models.CharField(max_length=50, blank=True, null=True)
    runtime = models.CharField(max_length=20, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    writer = models.CharField(max_length=255, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    production = models.CharField(max_length=255, blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)

    def get_info(self, title):
        # populate movie with information retrieved from OMDB API
        # http://www.omdbapi.com
        data = get_movie_information(title)

        self.title = data['title']
        self.year = data['year']
        self.rated = data['rated']
        self.released = data['released']
        self.runtime = data['runtime']
        self.genre = data['genre']
        self.director = data['director']
        self.writer = data['writer']
        self.actors = data['actors']
        self.plot = data['plot']
        self.production = data['production']
        self.poster_url = data['poster_url']

        self.save()

    def __str__(self):
        return '{} - directed by {}; {}'.format(self.title, self.director, self.released)


class Review(models.Model):

    author = models.ForeignKey('auth.User')
    movie = models.ForeignKey(Movie)
    title = models.CharField(max_length=255, default='Not specified!')
    body = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.review_date = timezone.now()
        self.save()

    def __str__(self):
        return '{}, {}'.format(self.title, self.author)


class Person(models.Model):

    name = models.CharField(max_length=255)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    signup_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    watch_list = models.ManyToManyField(Movie)

    def __str__(self):
        return '{}, {}'.format(self.user.username, self.signup_date)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

User._meta.get_field('username')._iexact = True
User._meta.get_field('email')._iexact = False