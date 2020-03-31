import requests
from flask import Flask , request , jsonify
import json
import time
from datetime import date , datetime
import xmlrpc.client
from graphene.test import Client
from data import setup
from schema import schema
import hprose
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost' , port=5672))
channel = connection.channel()

channel.queue_declare(queue='weatherUpdates')
        
app = Flask(__name__)

@app.route('/')
def hello_world():
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val =  ''+str(date)+ '-' + request.path +'\n'
    log.write(log_val)
    return 'Hello, World!'

@app.route('/insert', methods = ['GET','POST'])
def insert_record():
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    sid= request.args.get('sid')

    insert = open('students.log', 'a')
    date = datetime.now()
    insert_val =  ''+str(date)+ '-' + firstname+ '-' + lastname + '-' + sid +'\n'
    insert.write(insert_val) 

    log = open('calls.log', 'a')
    log_val =  ''+str(date)+ '-' + request.path +'\n'
    log.write(log_val)
    
    insert.close()

    output = [{ "user" : {
        "name" : firstname + ' ' + lastname,
        "student no": sid,
        "created": str(date.now())
    }}]
    return jsonify(output)
    
@app.route('/justweather')
def justweather_call():
    x = requests.get('http://kylegoslin.pythonanywhere.com/').json()

    date = datetime.now()
    log = open('calls.log', 'a')
    log_val =  ''+str(date)+ '-' + request.path +'\n'
    log.write(log_val)

    # parsed JSON content
    output = [{"forecast" : x['forecast']}]
    
    # adding a little markup
    return  jsonify(output)
    
@app.route('/updates')
def justupdates_call():
    f = open('updates.txt', 'r')
    x = f.readlines()
    output = []
    
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val =  ''+str(date)+ '-' + request.path +'\n'
    log.write(log_val)

    for item in x:
        #   "line1": "item1",
        obj = {"line" : item.strip() }
        output.insert(1,obj)
    f.close()

    return jsonify(output)

@app.route('/ping')
def ping():
    
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val =  ''+str(date)+ '-' + request.path +'\n'
    log.write(log_val)

    print('pong')
    return 'pong'

@app.route('/callClient')
def call_client():
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val =  ''+str(date)+ '-' + request.path +'\n'
    log.write(log_val)
    with xmlrpc.client.ServerProxy("http://127.0.0.1:8001/") as proxy:
        res = proxy.getTemp(3)
        print(res)
        output = [{"temp" : res}]
        return jsonify(output)

@app.route('/graphQL')
def graph_ql():
    date = datetime.now()
    log = open('calls.log', 'a')
    log_val =  ''+str(date)+ '-' + request.path +'\n'
    log.write(log_val)

    setup()
    client = Client(schema)

    query = """
        query FetchIdQuery($id: String!){
            student(id: $id){
                name
            }
        }
    """
    params = {"id": "1"}
    result = client.execute(query, variables=params)
    return result

@app.route('/ip')
def hprose_c():
    client = hprose.HttpClient('http://127.0.0.1:8080/')
    output = [{"node_server" : {"server ip address" : client.ping()}}]
    return jsonify(output)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(
    queue='weatherUpdates', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()