import pandas as pd

# Load Movies Metadata
metadata = pd.read_csv('D:\Github\Proyecto-IA\movie_metadata.csv', low_memory=False)

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

#Print the top 15 movies
q_movies[['movie_title', 'num_voted_users', 'imdb_score', 'score']].head(20)
