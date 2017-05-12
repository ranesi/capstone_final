from django.conf.urls import url
from . import views

urlpatterns = [

    # Homepage ############################################################

    url(r'^$', views.homepage, name='homepage'),

    # Farvell
    url(
        r'^logout_message/$',
        views.logout_message,
        name='logout_message'
    ),

    # Reviews #############################################################

    url(
        r'^reviews/all/$',
        views.show_reviews,
        name='show_reviews'
    ),
    url(
        r'^reviews/(?P<review_pk>\d+)/$',
        views.review_detail,
        name='review_detail'
    ),
    url(
        r'^review/add/(?P<movie_pk>\d+)/$',
        views.add_review,
        name='add_review'
    ),

    # Movies ##############################################################

    url(
        r'^movies/all$',
        views.show_movies,
        name='show_movies'
    ),
    url(
        r'^movies/add$',
        views.add_movie,
        name='add_movie'
    ),
    url(
        r'^movies/(?P<movie_pk>\d+)/$',
        views.movie_detail,
        name='movie_detail'
    ),

    url(
        '^watchlist/$',
        views.watchlist,
        name='watchlist'
    ),

    # People ##############################################################

    url(
        r'^people/all$',
        views.show_people,
        name='show_people'
    ),
    url(
        r'^people/search$',
        views.add_people,
        name='search_people'
    ),
    url(
        r'^people/(?P<person_pk>\d+)$',
        views.people_detail,
        name='people_detail'
    ),

]
