#!/usr/bin/env python
from flask import Flask, request, jsonify
from waitress import serve
from flask_cors import CORS  # Import CORS
import os
 
from function import handler
 
app = Flask(__name__)
CORS(app)  # Enable CORS for the app
 
class Event:
    def __init__(self):
        self.body = request.get_data()
        self.headers = request.headers
        self.method = request.method
        self.query = request.args
        self.path = request.path
 
class Context:
    def __init__(self):
        self.hostname = os.getenv('HOSTNAME', 'localhost')
 
def format_status_code(resp):
    if 'statusCode' in resp:
        return resp['statusCode']
     
    return 200
 
def format_body(resp):
    if 'body' not in resp:
        return ""
    elif type(resp['body']) == dict:
        return jsonify(resp['body'])
    else:
        return str(resp['body'])
 
def format_headers(resp):
    if 'headers' not in resp:
        return []
    elif type(resp['headers']) == dict:
        headers = []
        for key in resp['headers'].keys():
            header_tuple = (key, resp['headers'][key])
            headers.append(header_tuple)
        return headers
     
    return resp['headers']
 
def format_response(resp):
    if resp is None:
        return ('', 200)
 
    statusCode = format_status_code(resp)
    body = format_body(resp)
    headers = format_headers(resp)
 
    return (body, statusCode, headers)
 
def preprocess_headers(event):
    header_dict = dict(event.headers)
    for key in header_dict:
        os.environ['Http_' + key.upper().replace('-', '_')] = header_dict[key]
 
@app.route('/', defaults={'path': ''}, methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def call_handler(path):
    event = Event()
    context = Context()
    preprocess_headers(event)
    response_data = handler.handle(event, context)
     
    resp = format_response(response_data)
    return resp
 
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
