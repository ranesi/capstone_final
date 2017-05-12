from django import forms
from .models import Movie, Review, Person, Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'body', 'rating']


class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', ]


class AddToWatchListForm(forms.Form):

    add_box = forms.BooleanField(
        label='Add to List',
        required=True,
        initial=False,
    )


class SearchMoviesForm(forms.Form):

    search_term = forms.CharField(label='Title', max_length=255)


class SearchReviewsForm(forms.Form):

    search_term = forms.CharField(label='Title', max_length=255)


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('You must enter a username!')

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Username exists!')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email existing!')

        return email

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
