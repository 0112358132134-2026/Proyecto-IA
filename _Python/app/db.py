import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyecto_ia"
)

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
        sql = f"SELECT * FROM userpreferences WHERE UserId ='{user}'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    except:
        return None