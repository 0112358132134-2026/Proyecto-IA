from unicodedata import name
import pandas as pd

# Load Movies Metadata
metadata = pd.read_csv('C:/Users/68541/Documents/URL/1er. Ciclo 2022/Inteligencia Artificial/Proyecto/Proyecto-IA/_Python/app/movie_metadata.csv', low_memory=False)

# Print the first three rows
metadata.head(3)

#Calcular la media del promedio de votos
C = metadata['imdb_score'].mean()
print(C)

# Calcular el número nínimo de votos requeridos para ser aceptado
m = metadata['num_voted_users'].quantile(0.90)
print(m)

# Function that computes the weighted rating of each movie
def weighted_rating(x, m=m, C=C):
    v = x['num_voted_users']
    R = x['imdb_score']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)

# Define a new feature 'score' and calculate its value with `weighted_rating()`
q_movies = metadata.copy().loc[metadata['num_voted_users'] >= m]
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

#Sort movies based on score calculated above
q_movies = q_movies.sort_values('score', ascending=False)

#Return the top 15 movies
names = []
usersVotes = []
imdbScore = []
score = []
qmovies2 = q_movies[['movie_title', 'num_voted_users', 'imdb_score', 'score']].head(25)
for value in qmovies2['movie_title']:    
    names.append(value)
for value in qmovies2['num_voted_users']:    
    usersVotes.append(value)
for value in qmovies2['imdb_score']:    
    imdbScore.append(value)
for value in qmovies2['score']:    
    score.append(value)
movies = []
counter = 0
while counter < 25:
    movie = []
    movie.append(names[counter])
    movie.append(usersVotes[counter])
    movie.append(imdbScore[counter])
    movie.append(score[counter])
    movies.append(movie)
    counter += 1

counter = 0
for movie in movies:
    counter += 1
    print(str(counter) + " " + str(movie))