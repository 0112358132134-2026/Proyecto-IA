import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto_ia"
)

def csvExist():
    mycursor = mydb.cursor()
    sql = "SELECT id FROM csv LIMIT 1"
    mycursor.execute(sql)
    csvExist = mycursor.fetchall()
    if len(csvExist) == 1:
        return "1"
    return "0"

def userStatus(user, password, option):

    mycursor = mydb.cursor()
    result = 0

    query = f"SELECT User FROM user WHERE User = '{user}' LIMIT 1"                    
    mycursor.execute(query)
    userExist = mycursor.fetchall()

    if option == 1:
                        
        if len(userExist) == 1:
            return 1                    
        #query = f"SELECT * FROM User"
        #mycursor.execute(query)
        #users = mycursor.fetchall()

        #if len(users) > 0 and len(userExist) == 0:            
        #    result = 2
        #elif len(users) == 0 and len(userExist) == 0:            
        #    result = 3
        
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

def loadCSV(file):
    try: #Debemos agregar que cargue a pesar de errores
        df = pd.read_csv(file)        
        counter = 0
        for i in range(len(df.index)):

            mycursor = mydb.cursor()
            sql = "INSERT INTO csv (id, other) VALUES (%s, %s)"
            val = (df.iloc[counter]['movie_title'],df.iloc[counter]['imdb_score'])
            mycursor.execute(sql, val)
            mydb.commit()

            counter += 1
            if counter == 5000:
                break
        return "1"
    except:
        return "0"

def reloadCSV(file):        
    try:
        df = pd.read_csv(file)
        mycursor = mydb.cursor()
        sql = "INSERT INTO csv (id, other) VALUES (%s, %s)"
        val = (df.iloc[0]['movie_title'],df.iloc[0]['imdb_score'])
        mycursor.execute(sql, val)
        mydb.commit()
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
        sql = "INSERT INTO csv (id, other) VALUES (%s, %s)"
        val = (df.iloc[counter]['movie_title'],df.iloc[counter]['imdb_score'])
        mycursor.execute(sql, val)
        mydb.commit()

        counter += 1
        if counter == 5000:
            break
    return "1"

def SavePreference(user, movie, value):
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO user_preferences (UserId, MovieId, Value) VALUES (%s, %s, %s)"
        val = (user, movie, value)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    except:
        return False

def GetPreferences(user):
    try:
        mycursor = mydb.cursor()
        sql = f"SELECT * FROM user_preferences WHERE UserId ='{user}'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    except:
        return None