import pandas as pd

from db import UserPreferences, AllMoviesInfo


def GetRecommendation(user):
    RatedMovies = UserPreferences(user)
    allMovies = AllMoviesInfo()
    for movie in RatedMovies:

    return 0