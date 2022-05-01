import pandas as pd

from db import UserPreferences, AllMoviesInfo

def showRecommendations(exist, user):
    if exist == 0:
        #convertir Lista de listas a DataFrame
        metadata = pd.DataFrame(newReg, columns=['Movie Title','Director', 'Genres','Actors','keywords','IMDB score','User votes'])
        #Algoritmo Simple
        newReg = ToSimplexFormat(metadata)
        return simplexAlgorithm(newReg)
    else:
        return simplexAlgorithm(ComplexAlgorithm(user))

def ToSimplexFormat(registers):
    newRegisters = []
    for register in registers:
        _newRegister = []
        #Title, Director, Genres, Actors, KeyWords
        _newRegister.append(register[0], register[1], register[2], register[3], register[4])
        #imdb_score
        _newRegister.append(int(register[5]))
        #num voted users
        _newRegister.append(float(register[6]))
        #soup
        _newRegister.append(register[7])
        #Se agrega a la lista de listas
        newRegisters.append(_newRegister)
    return newRegisters

def simplexAlgorithm(newReg):
    #Calcular la media del promedio de votos
    C = metadata['IMDB score'].mean()
    print(C)

    # Calcular el número nínimo de votos requeridos para ser aceptado
    m = metadata['User votes'].quantile(0.90)
    print(m)

    # Function that computes the weighted rating of each movie
    def weighted_rating(x, m=m, C=C):
        v = x['User votes']
        R = x['IMDB score']
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)

    # Define a new feature 'score' and calculate its value with `weighted_rating()`
    q_movies = metadata.copy().loc[metadata['User votes'] >= m]
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

    #Sort movies based on score calculated above
    q_movies = q_movies.sort_values('score', ascending=False)

    #Return the top 15 movies
    names = []
    usersVotes = []
    imdbScore = []
    score = []
    qmovies2 = q_movies[['Movie Title','Director', 'Genres','Actors','keywords','IMDB score','User votes', 'score']].head(25)
    #for value in qmovies2['Movie Title']:
    #    names.append(value)
    #for value in qmovies2['User votes']:
    #    usersVotes.append(value)
    #for value in qmovies2['IMDB score']:
    #    imdbScore.append(value)
    #for value in qmovies2['score']:
    #    score.append(value)
    movies = []
    #counter = 0
    #while counter < 25:
    #    movie = []
    #    movie.append(names[counter])
    #    movie.append(str(usersVotes[counter]))
    #    movie.append(str(imdbScore[counter]))
    #    movie.append(str(score[counter]))
    #    movies.append(movie)
    #    counter += 1
    for i in range(len(qmovies2)):
        movie = [qmovies2.loc[i,'Movie Title'],
        qmovies2.loc[i,'Director'],
        qmovies2.loc[i,'Genres'],
        qmovies2.loc[i,'Actors'],
        qmovies2.loc[i,'keywords'],
        qmovies2.loc[i,'IMDB score'],
        qmovies2.loc[i,'User votes'],
        qmovies2.loc[i,'score'],
        ]
        movies.append(movie)
        #print("Total income in "+ df.loc[i,"Date"]+ " is:"+str(df.loc[i,"Income_1"]+df.loc[i,"Income_2"]))
    return movies

def ComplexAlgorithm(user):
    RatedMovies = UserPreferences(user)
    allMovies = AllMoviesInfo()
    #Soups
    LikedMoviesSoups = []
    UnlikedMoviesSoups = []
    #Get Info
    for movie in allMovies:
        if movie[0] in RatedMovies.keys():
            if RatedMovies[movie[0]] == '1':
                LikedMoviesSoups.append(movie[7])
            else:
                UnlikedMoviesSoups.append(movie[7])
    #DataFrame de todas las pelis
    df = pd.DataFrame(RatedMovies,columns=['Movie Title','Director', 'Genres','Actors','keywords','IMDB score','User votes', 'score'])
    #Algoritmo ()

    #q_movies = df.sort_values('prob', ascending=False)
    return 'Primeras pelis recomendadas en un DataFrame'