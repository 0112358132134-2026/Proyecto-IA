from flask import Flask, request
import json
import db
import complex_algorithms as ca

app = Flask(__name__)

@app.route('/csvExist', methods=['POST'])
def csvExist():    
    return db.csvExist()

@app.route('/loadCSV', methods=['POST'])
def loadCSV():
    response = request.data.decode("utf-8")    
    csv = json.loads(response)        
    result = db.loadCSV(csv['file'])
    return result

@app.route('/reloadCSV', methods=['POST'])
def reloadCSV():
    response = request.data.decode("utf-8")
    csv = json.loads(response)       
    result = db.reloadCSV(csv['file'])
    return result  

@app.route('/userStatus', methods=['POST'])
def userStatus():
    response = request.data.decode("utf-8")    
    user = json.loads(response)    
    print(user)
    status = db.userStatus(user['user'],user['password'],user['option'])
    return str(status)

@app.route('/showAllMovies', methods=['POST'])
def showAllMovies():            
    movies = db.showAllMovies()
    result = {
        "allMovies" : movies,
        "searchedMovies" : []
    }    
    return result

@app.route('/movieSearch', methods=['POST'])
def movieSearch():
    response = request.data.decode("utf-8")    
    toSearch = json.loads(response)    
    result = db.movieSearch(toSearch['name'])    
    movies = {
        "allMovies" : [],
        "searchedMovies" : result
    }
    return movies

@app.route('/addRating', methods=['POST'])
def addRating():
    response = request.data.decode("utf-8")    
    vote = json.loads(response)
    print(vote)  
    db.addRating(vote['user'],vote['movie'],vote['vote'])    
    return "OK"

@app.route('/userHasLikes', methods=['POST'])
def userHasLikes():
    response = request.data.decode("utf-8")    
    user = json.loads(response)
    print(user)     
    result = db.userHasLikes(user['user'])
    return result

@app.route('/showRecommendations', methods=['POST'])
def showRecommendations():
    response = request.data.decode("utf-8")    
    user = json.loads(response)  
    print(user)  
    recommendations = ca.showRecommendations(user['exist'],user['user'])   
    result = {
        "allMovies" : recommendations,
        "searchedMovies" : []
    } 
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)    