import mysql.connector
from numpy import moveaxis
import pandas as pd

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

def UserPreferences(user):
    mycursor = mydb.cursor()
    sql = f"SELECT MovieId, Value FROM user_preferences WHERE UserId ='{user}'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    movies = []
    for result in results:
        for movie in result:
            movies.append(movie)
    return movies