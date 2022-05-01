import mysql.connector
import pandas as pd
from sympy import false
import preferences_algorithms as pa

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto_ia"
)

def csvExist():
    mycursor = mydb.cursor()
    sql = "SELECT movie_title FROM csv LIMIT 1"
    mycursor.execute(sql)
    csvExist = mycursor.fetchall()
    if len(csvExist) == 1:
        return "1"
    return "0"

def loadCSV(file):
    try:
        df = pd.read_csv(file)
    except:
        return "0"
    df = pd.read_csv(file)    
    counter = 0    
    for i in range(len(df.index)):
        mycursor = mydb.cursor()
        try:
            sql = "INSERT INTO csv (movie_title, num_voted_users,imdb_score,director_name,actor_1_name,actor_2_name,actor_3_name,genres,plot_keywords) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (df.iloc[counter]['movie_title'],str(df.iloc[counter]['num_voted_users']),str(df.iloc[counter]['imdb_score']),df.iloc[counter]['director_name'],df.iloc[counter]['actor_1_name'],df.iloc[counter]['actor_2_name'],df.iloc[counter]['actor_3_name'],df.iloc[counter]['genres'],df.iloc[counter]['plot_keywords'])
            mycursor.execute(sql, val)
            mydb.commit()
            counter += 1                        
        except:            
            counter += 1
        if counter == 5000:
            break           
    return "1" 

def reloadCSV(file):        
    try:
        df = pd.read_csv(file)
    except:
        return "0"

    df = pd.read_csv(file)
    mycursor = mydb.cursor()
    sql = "DELETE FROM csv"    
    mycursor.execute(sql)
    mydb.commit()

    counter = 0
    for i in range(len(df.index)):
        mycursor = mydb.cursor()
        try:
            sql = "INSERT INTO csv (movie_title, num_voted_users,imdb_score,director_name,actor_1_name,actor_2_name,actor_3_name,genres,plot_keywords) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (df.iloc[counter]['movie_title'],str(df.iloc[counter]['num_voted_users']),str(df.iloc[counter]['imdb_score']),df.iloc[counter]['director_name'],df.iloc[counter]['actor_1_name'],df.iloc[counter]['actor_2_name'],df.iloc[counter]['actor_3_name'],df.iloc[counter]['genres'],df.iloc[counter]['plot_keywords'])
            mycursor.execute(sql, val)
            mydb.commit()       
            counter += 1            
        except:            
            counter += 1        
        if counter == 5000:            
            break    
    return "1"

def userStatus(user, password, option):

    mycursor = mydb.cursor()    
    query = f"SELECT User FROM user WHERE User = '{user}' LIMIT 1"                    
    mycursor.execute(query)
    userExist = mycursor.fetchall()

    if option == 1:
                        
        if len(userExist) == 1:
            return 1                            
        
        query= "INSERT INTO user (User, Password) VALUES (%s, %s)"
        val = (user,password)
        mycursor.execute(query,val)
        mydb.commit()
        return 2

    elif option == 2:
        
        if len(userExist) == 0:
            return 2
    
        query= f"SELECT User FROM user WHERE User = '{user}' AND Password = '{password}' LIMIT 1"                    
        mycursor.execute(query)
        userOK = mycursor.fetchall()
        if len(userOK) == 1:
            return 4
        else:
            return 3

def showAllMovies():
    mycursor = mydb.cursor()
    sql = "SELECT movie_title, director_name, genres, imdb_score FROM csv"
    mycursor.execute(sql)
    movies = mycursor.fetchall()

    if len(movies) == 0:
        return "0"           
    return movies

def movieSearch(name):
    mycursor = mydb.cursor()
    sql = f"SELECT movie_title FROM csv WHERE movie_title LIKE '%{name}%'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    movies = []
    for result in results:            
        for movie in result:
            movies.append(movie)
    return movies

def addRating(user, movie, vote):    
    copyMovie = movie
    if "'" in movie:
        movie = movie.replace("'","\\\'")
    mycursor = mydb.cursor()
    sql = f"SELECT MovieId FROM user_preferences WHERE UserId = '{user}' AND MovieId = '{movie}'"
    mycursor.execute(sql)
    register = mycursor.fetchall()
    if len(register) != 0: #Si existe, se elimina        
        query= f"DELETE FROM user_preferences WHERE UserId = '{user}' AND MovieId = '{movie}'"      
        mycursor.execute(query)
        mydb.commit()   
    query= "INSERT INTO user_preferences (UserId, MovieId, Value) VALUES (%s, %s, %s)"
    val = (user,copyMovie,vote)
    mycursor.execute(query,val)
    mydb.commit()

def userHasLikes(user):
    mycursor = mydb.cursor()
    sql = f"SELECT UserId FROM user_preferences WHERE UserId = '{user}'"
    mycursor.execute(sql)
    exist = mycursor.fetchall()
    if len(exist) != 0:
        return "1"
    return "0"

def simplexAlgorithm():
    mycursor = mydb.cursor()
    sql = f"SELECT movie_title,num_voted_users,imdb_score FROM csv"
    mycursor.execute(sql)
    registers = mycursor.fetchall()
    newRegisters = []
    for register in registers:
        _newRegister = []
        _newRegister.append(register[0])
        _newRegister.append(int(register[1]))
        _newRegister.append(float(register[2]))
        newRegisters.append(_newRegister)

    # Load Movies Metadata
    metadata = pd.DataFrame(newRegisters, columns=['movie_title','num_voted_users','imdb_score'])

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
        movie.append(str(usersVotes[counter]))
        movie.append(str(imdbScore[counter]))
        movie.append(str(score[counter]))
        movies.append(movie)
        counter += 1
    return movies

def showRecommendations(exist):
    if exist == 0:
        return simplexAlgorithm()
    return "Algoritmo complejo"

def UserPreferences(user: object) -> object:
    mycursor = mydb.cursor()
    sql = f"SELECT MovieId, Value FROM user_preferences WHERE UserId ='{user}'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    Diccionario = {}
    for result in results:
        Diccionario[result[0]] = [result[1]]
    return Diccionario

def AllMoviesInfo():
    mycursor = mydb.cursor()
    sql = "SELECT movie_title, director_name, genres, actor_1_name, actor_2_name, " \
          "actor_3_name, plot_keywords, imdb_score, num_voted_users FROM csv"
    mycursor.execute(sql)
    movies = mycursor.fetchall()

    if len(movies) == 0:
        return "0"
    return movies

