import requests
import json

def get_movie_information(title):
    r = requests.get(format_request(title))
    data = json.loads(r.text)
    try:
        # According to benchmarks, it is ~6x faster to declare a dict object using
        # '{}' than dict()
        ret = {
            'title': data['Title'],
            'year': data['Year'],
            'rated': data['Rated'],
            'released': data['Released'],
            'runtime': data['Runtime'],
            'genre': data['Genre'],
            'director': data['Director'],
            'writer': data['Writer'],
            'actors': data['Actors'],
            'plot': data['Plot'],
            'production': data['Production'],
            'poster_url': data['Poster']
        }
        # ret = dict(
        #     title=data['Title'],
        #     year=data['Year'],
        #     rated=data['Rated'],
        #     released=data['Released'],
        #     runtime=data['Runtime'],
        #     genre=data['Genre'],
        #     director=data['Director'],
        #     writer=data['Writer'],
        #     actors=data['Actors'],
        #     plot=data['Plot'],
        #     production=data['Production'],
        #     poster_url=data['Poster'],
        # )
        return ret
    except KeyError:
        return None


def movie_exists(title):
    r = requests.get(format_request(title))
    data = json.loads(r.text)
    if 'Error' in data:
        return False
    else:
        return True


def format_request(title):
    url = 'http://www.omdbapi.com/?t={}'
    return url.format(title)
