from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .omdb_api import movie_exists
from .forms import CreateUserForm, AddReviewForm, SearchMoviesForm, AddMovieForm, AddToWatchListForm
from .models import Review, Movie, Profile

# Create your views here.


def homepage(request):
    """Default view; renders homepage"""
    reviews = Review.objects.all().order_by('review_date').reverse()

    return render(request, 'trashflix/home.html', {'reviews': reviews})


@login_required
def show_reviews(request):
    """View showing all reviews for logged-in user"""
    reviews = Review.objects.all().filter(author=request.user)

    return render(request, 'trashflix/show_reviews.html', {'reviews': reviews})


@login_required
def review_detail(request, review_pk):

    review = get_object_or_404(Review, pk=review_pk)

    return render(request, 'trashflix/review_detail.html', {'review': review})


@login_required
def add_review(request, movie_pk):

    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'POST':

        form = AddReviewForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            review = Review.objects.create(author=request.user, movie=movie)

            review.title = data['title']
            review.body = data['body']
            review.rating = data['rating']

            review.publish()

            return redirect('trashflix:review_detail', review_pk=review.pk)

        else:

            return render(request, 'trashflix/add_review.html', {'form': form, 'movie': movie})

    else:
        form = AddReviewForm()

        return render(request, 'trashflix/add_review.html', {'form': form, 'movie': movie})


@login_required
def watchlist(request):

    profile = request.user.profile

    movies = profile.watch_list.all()

    return render(request, 'trashflix/show_watchlist.html', {'movies': movies})


@login_required
def add_movie(request):

    message = None

    if request.method == 'POST':

        form = AddMovieForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            title = data['title']

            if Movie.objects.filter(title__icontains=title).exists():

                message = "Movie already in database!"

                return render(request, 'trashflix/add_movie.html', dict(form=form, message=message))

            else:

                if movie_exists(title):

                    movie = Movie.objects.create()

                    movie.get_info(title)

                    return redirect('trashflix:movie_detail', movie_pk=movie.pk)

                else:

                    message = "Movie does not exist, apparently."

                    return render(request, 'trashflix/add_movie.html', {'form': form, 'message': message})
        else:
            return render(request, 'trashflix/add_movie.html', {'form': form, 'message': message})
    else:

        form = AddMovieForm()

        return render(request, 'trashflix/add_movie.html', {'form': form, 'message': message})



def show_movies(request):
    """Show list of movies; if movie does not exist, queries OMDB for movie info"""
    search_form = SearchMoviesForm()

    search_term = request.GET.get('search_term')

    if search_term:

        movies = Movie.objects.filter(
            title__icontains=search_term
        ).order_by(
            'title'
        )

        if not Movie.objects.filter(title__icontains=search_term):

            if movie_exists(search_term):

                movie = Movie.objects.create()

                movie.get_info(search_term)

                movies = Movie.objects.filter(pk=movie.pk)

    else:

        movies = Movie.objects.all().order_by(
            'title'
        )

    return render(request, 'trashflix/show_movies.html',
                  {'movies': movies, 'search_form': search_form})


@login_required
def movie_detail(request, movie_pk):

    movie = get_object_or_404(Movie, pk=movie_pk)

    message = None

    if request.method == 'POST':

        form = AddToWatchListForm(request.POST)

        if form.is_valid():

            profile = request.user.profile

            profile.watch_list.add(movie)

            profile.save()

            return redirect('trashflix:watchlist')

    else:

        form = AddToWatchListForm()

    return render(request, 'trashflix/movie_detail.html', {'movie': movie, 'form': form, 'message': message})


def show_people(request):
    # TODO
    pass


def add_people(request):
    # TODO
    pass


def people_detail(request, people_pk):
    # TODO
    pass


def register(request):
    """User registration view - logs in user if information is valid; redirect to homepage"""
    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password1']
            )

            login(request, user)

            return redirect('trashflix:homepage')

        else:

            return render(request, 'registration/register.html', {'form': form})

    else:

        form = CreateUserForm()

        return render(request, 'registration/register.html', {'form': form})


def logout_message(request):
    """Redirect from logout (?next= in template method)"""
    return render(request, 'trashflix/logout_message.html')
