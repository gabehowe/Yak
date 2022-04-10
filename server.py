import time
from typing import Dict, List
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# inboxes: Dict[str, List[dict]] = {'Jason1024': [{'from': 'joe', 'time': 1, 'content': 'hey, dude'}],
#                                   'joe': [{'from': 'Jason1024', 'time': 2, 'content': 'sup'}]}
inboxes = json.load(open('./messages.json'))
passwords = {'joe': '123ilovepizza', 'Jason1024': 'e'}


# for example: GET /messages?username=joe?password=123ilovepizza
@app.get("/messages")
def get_messages():
    username = request.args.get('username')
    password = request.args.get('password')
    if password != passwords[username]:
        return 401

    return jsonify(inboxes[username])


# POST /messages?destination=joe?from=jim with message json
@app.post("/messages")
def send_message():
    destination = request.args.get('destination')
    sender = request.args.get('from')
    if destination in inboxes.keys():
        message = request.get_json()
        if destination not in inboxes.keys():
            inboxes[destination] = []
        inboxes[destination].append({'from': sender, 'time': time.time_ns(), 'content': message['content']})
        with open('messages.json', 'w+') as file:
            file.write(json.dumps(inboxes))
        return message, 201

    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':
    app.run()
