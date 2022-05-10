from flask import Flask, session
from flask import jsonify, request
from pyparsing import removeQuotes
import repository
from model import Batch

def create_app(enviroment):
    app = Flask(__name__)
    return app

app =create_app()
session = repository.createSession()

@app.route('/add_batch/', methods=['POST'])
def create_batch():
    #session = repository.createSession()
    json = request.get_json(force=True)
    if json.get('reference') is None:
        return jsonify({'message': 'Bad request'}), 400
    batch = Batch(json['reference'],json['sku'], json['qty'],json['date'])
    session.add(batch)

@app.route('/get_batch/<ref>',methods=['GET'])
def edit_batch(ref):
    #session=repository.createSession()
    session.get(ref)

@app.route('/get_batch',methods=['GET'])
def edit_batch():
    #session=repository.createSession()
    json = request.get_json(force=True)
    session.list()
