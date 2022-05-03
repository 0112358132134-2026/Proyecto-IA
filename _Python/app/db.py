import mysql.connector
import pandas as pd
from sympy import false

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

    # Aplying trim to the titles
    print('Saving data...')
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())  

    errors = 0
    for i in range(len(df.index)):
        mycursor = mydb.cursor()
        try:
            sql = "INSERT INTO csv (movie_title, num_voted_users,imdb_score,director_name,actor_1_name,actor_2_name,actor_3_name,genres,plot_keywords, soup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (df.iloc[i]['movie_title'],str(df.iloc[i]['num_voted_users']),str(df.iloc[i]['imdb_score']),df.iloc[i]['director_name'],df.iloc[i]['actor_1_name'],df.iloc[i]['actor_2_name'],df.iloc[i]['actor_3_name'],df.iloc[i]['genres'],df.iloc[i]['plot_keywords'],'')
            mycursor.execute(sql, val)                      
        except:
            print(f'Error insertando, en la tupla: {i}')   
            errors += 1                 
    mydb.commit()   
    print(f'Registros con error: {errors}\n')

    #Cleaning data for soup
    print('Making soup...')
    metadata = pd.DataFrame(AllMoviesSoup(), columns=['movie_title', 'actor_1_name','actor_2_name','actor_3_name','director_name', 'plot_keywords', 'genres'])
    
    #Combine actors in a cast
    metadata['cast'] = metadata['actor_1_name'].str.cat(metadata[['actor_2_name', 'actor_3_name']], sep='|', na_rep='')
    
    #Converting many values in a list
    def converToList(feature):
        values = []
        for ind in metadata.index:
            current_list = str(metadata[feature][ind]).split('|')
            normalized_list = [x for x in current_list if pd.isnull(x) == False and x != '']
            values.append(normalized_list)
        return values

    features = ['cast', 'plot_keywords', 'genres']
    for feature in features:
        metadata[feature] = converToList(feature)

    #Cleaning data
    # Function to convert all strings to lower case and strip names of spaces
    def clean_data(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            #Check if director exists. If not, return empty string
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''
    
    features = ['cast', 'plot_keywords', 'director_name', 'genres']

    for feature in features:
        metadata[feature] = metadata[feature].apply(clean_data)

    def create_soup(x):
        return ' '.join(x['plot_keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director_name']

    # Create a new soup feature, falta eliminar el nan del registro 4
    metadata['soup'] = metadata.apply(create_soup, axis=1)

    # Create index to add soup
    metadata = metadata.reset_index()
    indices = pd.Series(metadata.index, index=metadata['movie_title'])
    
    moviesUpdate = metadata['movie_title']
    soups = 0
    for i in range(len(moviesUpdate)):
        mycursor = mydb.cursor()
        title = moviesUpdate[i]

        idx = indices[title]
        value = metadata.iloc[idx]['soup']
        try:
            sql = "UPDATE csv SET soup = %s WHERE movie_title = %s;"
            val = (value,title)
            mycursor.execute(sql, val)  
            soups += 1                  
        except:            
            print(f'Ha ocurrido un error en la soup: {i}') 
    mydb.commit()
    print(f'Soups creadas exitosamente: {soups}')
    return "1" 

def reloadCSV(file):        
    try:
        df = pd.read_csv(file)
    except:
        return "0"

    # Borrar datos de la tabla CSV
    df = pd.read_csv(file)
    mycursor = mydb.cursor()
    sql = "DELETE FROM csv"    
    mycursor.execute(sql)
    mydb.commit()

    mycursor = mydb.cursor()
    sql = "DELETE FROM user_preferences"    
    mycursor.execute(sql)
    mydb.commit()

    # Aplying trim to the titles
    print('Saving data...')
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())  

    errors = 0
    for i in range(len(df.index)):
        mycursor = mydb.cursor()
        try:
            sql = "INSERT INTO csv (movie_title, num_voted_users,imdb_score,director_name,actor_1_name,actor_2_name,actor_3_name,genres,plot_keywords, soup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (df.iloc[i]['movie_title'],str(df.iloc[i]['num_voted_users']),str(df.iloc[i]['imdb_score']),df.iloc[i]['director_name'],df.iloc[i]['actor_1_name'],df.iloc[i]['actor_2_name'],df.iloc[i]['actor_3_name'],df.iloc[i]['genres'],df.iloc[i]['plot_keywords'],'')
            mycursor.execute(sql, val)                      
        except:
            print(f'Error insertando, en la tupla: {i}')   
            errors += 1                 
    mydb.commit()   
    print(f'Registros con error: {errors}\n')

    #Cleaning data for soup
    print('Making soup...')
    metadata = pd.DataFrame(AllMoviesSoup(), columns=['movie_title', 'actor_1_name','actor_2_name','actor_3_name','director_name', 'plot_keywords', 'genres'])
    
    #Combine actors in a cast
    metadata['cast'] = metadata['actor_1_name'].str.cat(metadata[['actor_2_name', 'actor_3_name']], sep='|', na_rep='')
    
    #Converting many values in a list
    def converToList(feature):
        values = []
        for ind in metadata.index:
            current_list = str(metadata[feature][ind]).split('|')
            normalized_list = [x for x in current_list if pd.isnull(x) == False and x != '']
            values.append(normalized_list)
        return values

    features = ['cast', 'plot_keywords', 'genres']
    for feature in features:
        metadata[feature] = converToList(feature)

    #Cleaning data
    # Function to convert all strings to lower case and strip names of spaces
    def clean_data(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            #Check if director exists. If not, return empty string
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''
    
    features = ['cast', 'plot_keywords', 'director_name', 'genres']

    for feature in features:
        metadata[feature] = metadata[feature].apply(clean_data)

    def create_soup(x):
        return ' '.join(x['plot_keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director_name']

    # Create a new soup feature, falta eliminar el nan del registro 4
    metadata['soup'] = metadata.apply(create_soup, axis=1)

    # Create index to add soup
    metadata = metadata.reset_index()
    indices = pd.Series(metadata.index, index=metadata['movie_title'])
    
    moviesUpdate = metadata['movie_title']
    soups = 0
    for i in range(len(moviesUpdate)):
        mycursor = mydb.cursor()
        title = moviesUpdate[i]

        idx = indices[title]
        value = metadata.iloc[idx]['soup']
        try:
            sql = "UPDATE csv SET soup = %s WHERE movie_title = %s;"
            val = (value,title)
            mycursor.execute(sql, val)  
            soups += 1                  
        except:            
            print(f'Ha ocurrido un error en la soup: {i}') 
    mydb.commit()
    print(f'Soups creadas exitosamente: {soups}')
    return "1" 


    #counter = 0
    #for i in range(len(df.index)):
    #    mycursor = mydb.cursor()
    #    try:
    #        sql = "INSERT INTO csv (movie_title, num_voted_users,imdb_score,director_name,actor_1_name,actor_2_name,actor_3_name,genres,plot_keywords) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #        val = (df.iloc[counter]['movie_title'],str(df.iloc[counter]['num_voted_users']),str(df.iloc[counter]['imdb_score']),df.iloc[counter]['director_name'],df.iloc[counter]['actor_1_name'],df.iloc[counter]['actor_2_name'],df.iloc[counter]['actor_3_name'],df.iloc[counter]['genres'],df.iloc[counter]['plot_keywords'])
    #        mycursor.execute(sql, val)
    #        mydb.commit()       
    #        counter += 1            
    #    except:            
    #        counter += 1        
    #    if counter == 5000:            
    #        break    
    #return "1"

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

def UserPreferences(user: object) -> object:
    mycursor = mydb.cursor()
    sql = f"SELECT MovieId, Value FROM user_preferences WHERE UserId ='{user}'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    Diccionario = {}
    for result in results:
        Diccionario[result[0]] = result[1]
    return Diccionario

def AllMoviesInfo():
    mycursor = mydb.cursor()
    sql = "SELECT movie_title, director_name, genres, CONCAT(actor_1_name,', ', actor_2_name,', ', actor_3_name) AS actors," \
          "plot_keywords, imdb_score, num_voted_users, soup FROM csv"
    mycursor.execute(sql)
    movies = mycursor.fetchall()

    if len(movies) == 0:
        return "0"
    return movies

def AllMoviesSoup():

    mycursor = mydb.cursor()
    sql = "SELECT movie_title, actor_1_name, actor_2_name, actor_3_name, director_name, plot_keywords, genres FROM csv"
    mycursor.execute(sql)
    movies = mycursor.fetchall()
    if len(movies) == 0:
        return "0"
    return movies