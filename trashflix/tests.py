from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import IntegrityError
from .models import Movie, Review
from .forms import AddReviewForm, AddMovieForm, SearchMoviesForm, SearchReviewsForm, CreateUserForm
import re

##############################################################################
# Form tests
##############################################################################

class AddReviewFormTest(TestCase):

    def setUp(self):
        Movie.objects.create(title='asd')
        Movie.objects.create(title='zxc')
        User.objects.create(
            username='zxc',
            password='qwerqwer'
        )


    def test_no_title(self):

        mov = Movie.objects.get(title='asd')
        user = User.objects.get(username='zxc')

        test_form = dict(body='asdasdasd', movie=mov, author=user)

        form = AddReviewForm(test_form)

        self.assertFalse(form.is_valid())


    def test_no_body(self):

        mov = Movie.objects.get(title='asd')
        user = User.objects.get(username='zxc')

        test_form = dict(title='asdasdasd', movie=mov, author=user)

        form = AddReviewForm(test_form)

        self.assertFalse(form.is_valid())


    def test_title_too_long(self):

        mov = Movie.objects.get(title='asd')
        user = User.objects.get(username='zxc')

        test_form = dict(title='Q'*256, body='zxc', movie=mov, user=user)

        form = AddReviewForm(test_form)

        self.assertFalse(form.is_valid())


    def valid_review_form(self):

        movie = Movie.objects.get(title='asd')
        user = User.objects.get(username='zxc')

        test_form = dict(title='qwe', body='rty', movie=movie, user=user)

        form = AddReviewForm(test_form)

        self.assertTrue(form.is_valid())


class AddMovieFormTest(TestCase):

    def test_title_too_long(self):

        test_form = dict(title='Q'*256)

        form = AddMovieForm(test_form)

        self.assertFalse(form.is_valid())


    def valid_add_movie_form(self):

        test_form = dict(title='Deathspa')

        form = AddMovieForm(test_form)

        self.assertTrue(form.is_valid())


class SearchMovieFormTest(TestCase):

    def test_search_too_long(self):

        test_form = dict(search_term='q'*256)

        form = SearchMoviesForm(test_form)

        self.assertFalse(form.is_valid())


    def valid_movie_search(self):

        test_form = dict(search_term='Deathbed: The Bed that Eats')

        form = SearchMoviesForm(test_form)

        self.assertTrue(form.is_valid())


class SearchReviewsFormTest(TestCase):

    def test_search_too_long(self):

        test_form = dict(search_term='q'*256)

        form = SearchReviewsForm(test_form)

        self.assertFalse(form.is_valid())


    def valid_review_search(self):

        test_form = dict(search_term='LOL Movey Reveiw!1>')

        form = SearchReviewsForm(test_form)

        self.assertTrue(form.is_valid())


class CreateUserFormTest(TestCase):

    def setUp(self):
        user1_info = {
            'username': 'a',
            'email': 'b@b.gov',
            'password1': 'qwerqwer',
            'password2': 'qwerqwer'
        }
        user2_info = {
            'username': 'b',
            'email': 'c@c.gov',
            'password1': 'qwerqwer',
            'password2': 'qwerqwer'
        }

        user1 = User(user1_info)
        user2 = User(user2_info)

        user1.save()
        user2.save()


    def valid_user_creation_form(self):

        test_form = {
            'username': 'JimmyDean',
            'email': 'asd@asd.biz',
            'password1': 'zxcvzxcv',
            'password2': 'zxcvzxcv'
        }

        form = CreateUserForm(test_form)

        self.assertTrue(form.is_valid())


    def test_password_too_short(self):
        test_form = {
            'username': 'JimmyDean',
            'email': 'asd@asd.biz',
            'password1': 'zxcvzxv',
            'password2': 'zxcvzxv'
        }

        form = CreateUserForm(test_form)

        self.assertFalse(form.is_valid())


    def test_user_already_exists(self):
        test_form = {
            'username': 'a',
            'email': 'b@b.gov',
            'password1': 'qwerqwer',
            'password2': 'qwerqwer'
        }

        form = CreateUserForm(test_form)

        self.assertFalse(form.is_valid())


    def test_mismatching_password_invalid(self):
        test_form = {
            'username': 'JimmyDean',
            'email': 'asd@asd.biz',
            'password1': 'zxcvzxv',
            'password2': 'axcvzxv'
        }

        form = CreateUserForm(test_form)

        self.assertFalse(form.is_valid())

##############################################################################
# Model Tests
##############################################################################


class TestUserObject(TestCase):

    def test_user_required_fields(self):

        user = User(username=None)
        with self.assertRaises(IntegrityError):
            user.save()

        user = User(username='a')
        with self.assertRaises(IntegrityError):
            user.save()

        user = User(password='zxcvzxcv')
        with self.assertRaises(IntegrityError):
            user.save()


    def unique_username_required(self):
        user_info = dict(
            username='a',
            password='zxcvzxcv'
        )

        user1 = User(user_info)
        user1.save()

        user2 = User(user_info)
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_username_case_insensitive(self):

        u1 = dict(
            username='a',
            password='zxcvzxcv'
        )
        u2 = dict(
            username='A',
            password='zxcvzxcv'
        )

        user1 = User(u1)
        user1.save()

        user2 = User(u2)
        with self.assertRaises(IntegrityError):
            user2.save()

##############################################################################
# View tests
##############################################################################


# class TestViewsIfEmpty(TestCase):
#
#     def test_no_movies(self):
#
#         r = self.client.get(reverse('trashflix:show_movies'))
#         self.assertFalse(r.context['movies'])
#
#
#     def test_no_reviews(self):
#
#         r = self.client.get(reverse('trashflix:show_reviews'))
#         self.assertFalse(r.context['reviews'])

