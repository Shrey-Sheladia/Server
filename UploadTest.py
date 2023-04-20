import json
import requests
from datetime import datetime

URL = "http://172.31.23.209:5000"
def log_action(option_selected, session_id):
    now = datetime.now()

    info = {
        "Day" : now.strftime('%d/%m/%Y'),
        "Time" : now.strftime('%H:%M:%S'),
        "Info" : option_selected,
        "Session ID" : session_id
        }   
    info = json.dumps(info)
    now = datetime.now()
    log_entry = f"{now.strftime('%Y-%m-%d - %H:%M:%S')} | {session_id} | {option_selected}\n"
    print(log_entry, end = " - ")
    response = requests.post(URL, json=info)
    print(response.text, 1)

log_action("Options Here", "SomeUID")