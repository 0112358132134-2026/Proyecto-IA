import pandas as pd

from db import UserPreferences, AllMoviesInfo

def GetRecommendation(user):
    RatedMovies = UserPreferences(user)
    allMovies = AllMoviesInfo()
    ratedmoviescount = len(RatedMovies.keys())
    #Get Info
    for movie in allMovies:
        if movie[0] in RatedMovies.keys():
            #Director
            RatedMovies[movie[0]].append(movie[1])
            #Genres
            RatedMovies[movie[0]].append(movie[2])
            #Actor1
            RatedMovies[movie[0]].append(movie[3])
            #Actor2
            RatedMovies[movie[0]].append(movie[4])
            #Actor3
            RatedMovies[movie[0]].append(movie[5])
            #keywords
            RatedMovies[movie[0]].append(movie[6])
            #imdb score
            RatedMovies[movie[0]].append(movie[7])
            #num voted users
            RatedMovies[movie[0]].append(movie[8])
    resultD=DirectorFreq(RatedMovies)
    likedmoviescount = resultD[0]
    Directors = resultD[1]
    Actors=ActorFreq(RatedMovies)
    Genres=GenreFreq(RatedMovies)
    KeyWords=KeyWordFreq(RatedMovies)
    Recommended = Probabilities(allMovies,Directors,Actors,Genres,KeyWords,likedmoviescount, ratedmoviescount,RatedMovies)
    #print(sorted(allMovies, key=lambda movie: movie[9]))
    df = pd.DataFrame(Recommended,columns=['like', 'director', 'genres', 'actor1','actor2', 'actor3', 'keywords', 'imdb score', 'num voted users','prob'])
    q_movies = df.sort_values('prob', ascending=False)
    return q_movies.head(20)

def Probabilities(allMovies,Directors,Actors,Genres,KeyWords,likedmoviescount, ratedmoviescount,RatedMovies):
    RecommendedMovies = []
    for movie in allMovies:
        movie= list(movie)
        if movie[0] not in RatedMovies.keys():
            DirectorProb = NaiveBayes(Directors,movie[1].lower().replace(" ", ""),likedmoviescount, ratedmoviescount,2)
            GenresProb = 1
            for genre in movie[2].split("|"):
                GenresProb*=NaiveBayes(Genres,genre.lower().replace(" ", ""),likedmoviescount, ratedmoviescount,2)
            Actor1Prob = NaiveBayes(Actors,movie[3].lower().replace(" ", ""),likedmoviescount, ratedmoviescount,2)
            Actor2Prob = NaiveBayes(Actors,movie[4].lower().replace(" ", ""), likedmoviescount, ratedmoviescount,2)
            Actor3Prob = NaiveBayes(Actors,movie[5].lower().replace(" ", ""), likedmoviescount, ratedmoviescount,2)
            KeyWordsProb = 1
            for keyword in movie[6].split("|"):
                KeyWordsProb*=NaiveBayes(KeyWords,keyword.lower().replace(" ", ""), likedmoviescount, ratedmoviescount,2)
            movie.append(DirectorProb*GenresProb*Actor1Prob*Actor2Prob*Actor3Prob*KeyWordsProb)
            RecommendedMovies.append(movie)
    return RecommendedMovies

def NaiveBayes(Dictio, Evidence,likedmoviescount, ratedmoviescount, alpha):
    numerator = 1
    denominator = 1
    if Evidence in Dictio.keys():
        if Dictio[Evidence][0] != 0:
            numerator = (Dictio[Evidence][0]/likedmoviescount) * (likedmoviescount / ratedmoviescount)
            denominator = numerator + (Dictio[Evidence][1]/(ratedmoviescount-likedmoviescount)) * ((ratedmoviescount - likedmoviescount) / ratedmoviescount)
        else:
            numerator = alpha
            denominator = (ratedmoviescount) + (2 * alpha)
    else:
        numerator = alpha
        denominator = (ratedmoviescount) + (2 * alpha)
    return numerator/denominator

def DirectorFreq(RatedMovies):
    Directors = {}
    likedmoviescount = 0
    for key in RatedMovies.keys():
        like = RatedMovies[key][0]
        director = RatedMovies[key][1].lower().replace(" ", "")
        if director in Directors.keys():
            if like == 1:
                Directors[director][0] += 1
                likedmoviescount += 1
            else:
                Directors[director][1] += 1
        else:
            if like == 1:
                Directors[director]= [1,0]
                likedmoviescount += 1
            else:
                Directors[director] = [0, 1]
    return [likedmoviescount, Directors]

def ActorFreq(RatedMovies):
    Actors = {}
    for key in RatedMovies.keys():
        like = RatedMovies[key][0]
        cont = 3
        while cont < 6:
            actor = RatedMovies[key][cont].lower().replace(" ", "")
            if actor in Actors.keys():
                if like == 1:
                    Actors[actor][0] += 1
                else:
                    Actors[actor][1] += 1
            else:
                if like == 1:
                    Actors[actor] = [1, 0]
                else:
                    Actors[actor] = [0, 1]
            cont += 1
    return Actors

def GenreFreq(RatedMovies):
    Genres = {}
    for key in RatedMovies.keys():
        like = RatedMovies[key][0]
        genres = RatedMovies[key][2].split("|")
        for genre in genres:
            genre = genre.lower().replace(" ", "")
            if genre in Genres.keys():
                if like == 1:
                    Genres[genre][0] += 1
                else:
                    Genres[genre][1] += 1
            else:
                if like == 1:
                    Genres[genre] = [1, 0]
                else:
                    Genres[genre] = [0, 1]
    return Genres
def KeyWordFreq(RatedMovies):
    KeyWords={}
    for key in RatedMovies.keys():
        like = RatedMovies[key][0]
        keywords = RatedMovies[key][6].split("|")
        for keyword in keywords:
            keyword = keyword.lower().replace(" ", "")
            if keyword in KeyWords.keys():
                if like == 1:
                    KeyWords[keyword][0] += 1
                else:
                    KeyWords[keyword][1] += 1
            else:
                if like == 1:
                    KeyWords[keyword] = [1, 0]
                else:
                    KeyWords[keyword] = [0, 1]
    return KeyWords
print(GetRecommendation("jdeleon"))