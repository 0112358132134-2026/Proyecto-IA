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
            if RatedMovies[movie[0]] == 1:
                LikedMoviesSoups.append(movie[7])
            else:
                UnlikedMoviesSoups.append(movie[7])
    #DataFrame de todas las pelis
    metadata = pd.DataFrame(allMovies, columns=['Movie Title','Director', 'Genres','Actors','keywords','IMDB score','User votes', 'Soup'])
    
    # Probabilities
    total_sentences = len(LikedMoviesSoups) + len(UnlikedMoviesSoups)

    p_like = len(LikedMoviesSoups)/total_sentences;
    p_unlike = len(UnlikedMoviesSoups)/total_sentences;

    # Frecuencias (Bag of words)
    def create_table_freq(corpus):
        freq = {}
        for sent in corpus:
            tokens = sent.split(' ')
            for token in tokens:
                if token not in freq.keys():
                    freq[token] = 1
                else:
                    freq[token] += 1
        return freq

    freq_like = create_table_freq(LikedMoviesSoups)
    freq_unlike = create_table_freq(UnlikedMoviesSoups)

    # Obteniendo probabilidades de cada palabra
    def count_words(corpus):
        freq = 0
        for sent in corpus:
            freq += len(sent.split(' '))
        return freq

    total_like = count_words(LikedMoviesSoups)
    total_unlike = count_words(UnlikedMoviesSoups)

    # Transform to Cpt's
    def create_cpt(freq, total):
        cpt_eqv = {}
        for k,v in freq.items():
            probability = v/total
            cpt_eqv[k] = probability
        return cpt_eqv

    cpt_like = create_cpt(freq_like, total_like)
    cpt_unlike = create_cpt(freq_unlike, total_unlike)

    def calcLike(texto, alpha):
        p_cadena_like = 1
        p_cadena_unlike = 1
        oracion = texto.split(' ')
        for i in range(len(oracion)):
            if oracion[i] not in cpt_like:
                laplace1 = alpha / ((total_like+total_unlike)+(2*alpha))
                p_cadena_like *=  laplace1
            else:
                p_cadena_like *=  cpt_like[oracion[i]]
            if oracion[i] not in cpt_unlike:
                laplace2 = alpha / ((total_like+total_unlike)+(2*alpha))
                p_cadena_unlike *=  laplace2
            else:
                p_cadena_unlike *=  cpt_unlike[oracion[i]]
        p_final = (p_cadena_like * p_like) / ((p_cadena_like * p_like) + (p_cadena_unlike * p_unlike))
        return p_final

    metadata = metadata.reset_index()
    indices = pd.Series(metadata.index, index=metadata['Movie Title'])

    def addRecomendation(title):
        idx = indices[title]
        idx_val = metadata.iloc[idx]['Soup']
        if isinstance(idx_val, str):
            return calcLike(idx_val, 1)
        else:
            norm = idx_val.values[0]
            return calcLike(norm, 1)

    all_movies = metadata['Movie Title']
    r_values = []

    for i in range(len(all_movies)):
        r_values.append(addRecomendation(all_movies[i]))

    metadata['Result'] = r_values
    prev = metadata[['Movie Title','Director', 'Genres','Actors','keywords','IMDB score','User votes','Result']].sort_values(by=['Result'],ascending=False)

    #Deleting repeatable values
    result = prev[~prev['Movie Title'].isin(RatedMovies.keys())]

    return result.head(20)