import argparse
import time
import tkinter
import requests
from threading import *

messages = []
old_messages = []


def send_message(content, destination):
    requests.post(f'http://127.0.0.1:5000/messages?destination={destination}&from={username}',
                  json={'content': content})
    print(content)


def get_messages():
    global old_messages, messages
    while True:
        time.sleep(1)
        request = requests.get(f'http://127.0.0.1:5000/messages?username={username}&password={password}')
        messages = request.json()
        new_messages = [i for i in messages if i not in old_messages]
        old_messages = messages
        for i in new_messages:
            # [time] Username: hey i just ate a big chocolate bar
            print(f'[{i["time"]}]{i["from"]}: {i["content"]}')


def main(args):
    get_thread = Thread(target=get_messages())
    get_thread.run()
    while True:
        message = input(': ')
        destination = input('@')
        send_message(message, destination)


parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()
username = args.username
password = args.password
main(args)
