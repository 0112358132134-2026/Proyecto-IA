from flask import Flask, jsonify
from flask import request
import db


app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({'message':'pong'})

#--------------- Login
@app.route('/createUser', methods=['POST'])
def getPreference():
    request_data = request.get_json()

    user = request_data['user']
    password = request_data['password']

    exists = db.ExistUser(user)
    if not exists:
        db.CreateUser(user, password)
        return 'Usuario registrado exitosamente!!!'
    else:
        return 'El usuario ya existe'

@app.route('/getPreferences', methods=['POST'])
def getPreference():
    request_data = request.get_json()

    user = request_data['user']
    result = db.GetPreferences(user)
    if result is not None:
        return jsonify(result)
    else:
        return 'Error'

@app.route('/insertPreference', methods=['POST'])
def insertPreference():
    request_data = request.get_json()

    user = request_data['user']
    movie = request_data['movie']
    value = request_data['value']
    result = db.SavePreference(user, movie, value)
    if result:
        return 'Información Guardada Existosamente!!!'
    else:
        return 'Error'
    

if __name__ == '__main__':
    app.run(debug = True, port = 4000)


