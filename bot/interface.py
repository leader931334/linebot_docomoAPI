import os
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

LINE_REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + LINE_ACCESS_TOKEN
}

def index(request):
    return HttpResponse("It works!")

def callback(request_json):
    reply = ""
    request = json.loads(request_json.body.decode('utf-8'))
    for e in request["events"]:
        reply_token = e["replyToken"]
        if e["type"] == "message":
            if e["message"]["type"] == "text":
                reply += e["message"]["text"]
            else:
                reply += "only text message"
            reply_message(reply_token, reply)
    return HttpResponse(reply)

def make_text():
    from . import reply_words
    return random.choice(reply_words)


def reply_message(reply_token, reply):
    reply_body = {
        "replyToken":reply_token,
        "messages":[
            {
                "type":"text",
                "text": reply
            }
        ]
    }
    requests.post(LINE_REPLY_ENDPOINT, headers=LINE_HEADER, data=json.dumps(reply_body))
