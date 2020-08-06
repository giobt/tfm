import sys
import json
import os
import time

from antlr4 import *
from flask import Flask
from flask import jsonify
from flask import request
from json import dumps
from kafka import KafkaProducer
from stix2validator import validate_instance
from werkzeug.http import HTTP_STATUS_CODES

app = Flask(__name__)

kafka_broker = os.environ.get('KAFKA_BROKER') or 'localhost:9092'
kafka_topic = os.environ.get('KAFKA_TOPIC') or 'numtest'

@app.route("/health")
def health():
    return {'message': 'Healthy'}

@app.route("/rule/create", methods=['POST'])
def create():
    # Start measuring execution time for evaluation purposes
    start_time = time.time()
    
    # Get STIX 2.1 bundle in json format
    data = request.get_json() or {}
    
    # Validate input
    validation = results = validate_instance(data)

    # Return errors if not valid STIX 2.1 format
    if not validation.is_valid:
        return bad_request(validation.errors[0].message)
    
    # Initialize kafka broker
    producer = KafkaProducer(bootstrap_servers=[kafka_broker],
                            value_serializer=lambda x: dumps(x).encode('utf-8'))

    # Send content to broker
    producer.send(kafka_topic, value=data)

    # Finish measuring execution time for evaluation purposes
    end_time = time.time()
    ellapsed_time = end_time - start_time

    # Return status code
    print("--- %s seconds ---" % (ellapsed_time))
    return {'message': 'Success', 'time': ellapsed_time}

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
    app.run(host='0.0.0.0', port=8080, debug=True)