import requests
import json
import os
import uuid
from dotenv import load_dotenv


load_dotenv()
if "CHANNEL" in os.environ:
    CHANNEL = os.environ['CHANNEL']
else:
    CHANNEL = "C04T4E5HC0G"

TOKEN = os.environ['SLACK_TOKEN']


def send_file(msg, img_bytes):
    headers = {    
        'Authorization': f"Bearer {TOKEN}"    
    }
    files = {'file': img_bytes }
    fname = "{}.png".format(uuid.uuid4())
    params = { 
        'channels': CHANNEL,
        'filename':fname,
        'filetype': 'png',
        'initial_comment': msg,    
    }
    r = requests.post(url="https://slack.com/api/files.upload", params=params, headers=headers, files=files)
    return r.text

def send_message(msg):
    headers = {
        "Content-type": "application/json",    
        "Authorization": 'Bearer {}'.format(TOKEN)
    }
    data = {
        "channel": CHANNEL,    
        "text": msg
    }

    r = requests.post(url="https://slack.com/api/chat.postMessage", data=json.dumps(data), headers=headers)    
    return r.text