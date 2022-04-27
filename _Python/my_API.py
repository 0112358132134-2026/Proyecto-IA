from re import I
from urllib import response
from flask import Flask, render_template, request
from requests import RequestException

app = Flask(__name__)

@app.route('/operate', methods=['GET'])
def operate():
    diccionario = {
        'name' : "holi",
        'ratio' : 6,
    }                   
    return diccionario

@app.route('/ola/<string:texto>', methods=['POST'])
def okNum(texto):            
    print(texto)
    if texto == "José":
        return "OK"
    else:
        return "F"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)