from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .omdb_api import movie_exists
from .forms import SearchMoviesForm, AddMovieForm, AddToWatchListForm
from .models import Movie

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
