from flask import Flask
from flask import jsonify
from flask import request
from json import dumps
from kafka import KafkaProducer
from time import sleep
from werkzeug.http import HTTP_STATUS_CODES

import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/rule/create", methods=['POST'])
def create():
    data = request.get_json() or {}
    
    # Validate input
    if 'Rule' not in data:
        return bad_request('must include Rule field')

    # Parse input into suricata rule format
    rule = parse_rule(data['Rule'])

    # Initialize kafka broker
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                            value_serializer=lambda x: dumps(x).encode('utf-8'))

    # Send rule to broker
    producer.send('numtest', value=rule)

    # Return status code
    return "response"

def parse_rule(data):
    options = ""
    for option in data['options']:
        options = options + "{key}: \"{value}\"; ".format(key=option, value=data['options'][option])

    modifiers = ""
    for modifier in data['modifiers']:
        modifiers = modifiers + modifier + "; "

    rule = "{action} {protocol} {src_ip} {src_port} {direction} {dst_ip} {dst_port} ({options}{modifiers})".format(
        action=data['action'],
        protocol=data['header']['protocol'],
        src_ip=data['header']['src_ip'],
        src_port=data['header']['src_port'],
        direction=data['header']['direction'],
        dst_ip=data['header']['dst_ip'],
        dst_port=data['header']['dst_port'],
        options=options,
        modifiers=modifiers)    

    return rule

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)

if __name__ == '__main__':
    app.run(debug=True)