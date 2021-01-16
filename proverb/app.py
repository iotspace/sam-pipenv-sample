import json
import random
import requests
import os
import urllib.parse


proverbs = [
    {"proverb": "It works on my machine",  "who_said": "Anonymous"},
    {"proverb": "Debugging code requires twice as much effort as writing. So you don't have the brains to debug the code you write to the fullest.", "who_said": "Brian Kernighan"},
    {"proverb": "If two programmers do what one programmer can do in one month, it will take two months.", "who_said": "Fred Brooks"},
    {"proverb": "Talking is good, show me your code", "who_said": "Linus Torvalds"}
]


def lambda_handler(event, context):
    # Funny toy app!
    proverb = random.choice(proverbs)
    proverb_text = f"Today's quote\n*「{proverb['proverb']}」* by {proverb['who_said']}"

    token = os.getenv("SLACK_TOKEN")
    channel = os.getenv("SLACK_CHANNEL")
    
    # result = SlackNotifier(token, channel).post(proverb_text)    
    result = EchoJson(token, channel).do_echo(proverb['proverb'], proverb['who_said'])  
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{result.text}",
        })
    }    
    


class EchoJson:
    """
    This class will use the Echo Json service online to demo test json values
    """
    # Endpoint: http://echo.jsontest.com/insert-key-here/insert-value-here/key/value
    ECHO_JSON_MESSAGE_URL = "http://echo.jsontest.com/"

    def __init__(self, token, channel_name):
        self.token = token
        self.channel_name = channel_name
        self.base_url = self.ECHO_JSON_MESSAGE_URL + "token/"+token + "/channel/"+ channel_name+"/"
    
    def do_echo(self, proverb_text, who_said):
        proverb_text_urlencoded = urllib.parse.quote(proverb_text)
        who_said_urlencoded = urllib.parse.quote(who_said)
        url = self.base_url + "proverb/"+proverb_text_urlencoded+"/who_said/"+who_said_urlencoded
        return requests.get(url=url)


class SlackNotifier:
    SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"

    def __init__(self, token, channel_name):
        self.token = token
        self.channel_name = channel_name

    def post(self, text):
        params = {
            "token": self.token,
            "channel": self.channel_name,
            "text": text,
            "unfurl_links": True
        }
        return requests.post(url=self.SLACK_POST_MESSAGE_URL, params=params)

