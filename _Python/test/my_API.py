from re import I
from urllib import response
from flask import Flask, render_template, request
from requests import RequestException
import json

app = Flask(__name__)

@app.route('/operate', methods=['GET'])
def operate():
    diccionario = {
        'name' : "holi",
        'ratio' : 6,
    }                   
    return diccionario

@app.route('/prueba/<string:usuario>', methods=['GET'])
def prueba_get(usuario):
    diccionario = {
        'name' : usuario,
        'ratio' : 6,
    }     
    print(usuario)
    return diccionario

@app.route('/ola/<string:texto>', methods=['POST'])
def okNum(texto):            
    print(texto)
    if texto == "José":
        return "OK"
    else:
        return "F"

@app.route('/userStatus', methods=['POST'])
def userStatus():

    response = request.data.decode("utf-8")    
    print(response)
    user = json.loads(response)
    print(user)
    if user['user'] == 'Pablo' and user['password'] == '1234':
        return "5"
    else:
        return "-1"    

@app.route('/firstUser', methods=['POST'])
def firstUser():

    response = request.data.decode("utf-8")    
    print(response)
    user = json.loads(response)
    
    print(user)
    
    diccionario = {
        'name' : "Pablo",
        'ratio' : 6,
    }         
    return diccionario    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)