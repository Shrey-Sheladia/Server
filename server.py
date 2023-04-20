import os
import json
import telebot
import threading
from flask import Flask, request


try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

API_KEY = os.environ.get("telegrambotAPI_key")
CHAT_ID = os.environ.get("CHAT_ID")

bot1 = telebot.TeleBot(API_KEY)

app = Flask(__name__)

@bot1.message_handler(commands=['get_file'])
def send_log_file(message):
    log_file_path = "data.json"
    if os.path.exists(log_file_path):
        with open(log_file_path, "rb") as log_file:
            bot1.send_document(chat_id=CHAT_ID, document=log_file, caption="data.json")
    else:
        bot1.reply_to(message, "data.json file not found")


def polling_thread():
    bot1.polling()

thread = threading.Thread(target=polling_thread)
thread.start()

@app.route('/data', methods=['GET'])
def get_data():
    with open("data.json") as f:
        data = json.load(f)
    return json.dumps(data)

@app.route('/update', methods=['POST'])
def update():
    new_data = json.loads(request.get_json())

    if "Start" in new_data:
        bot1.send_message(CHAT_ID, f"Website being used at {new_data['Start']}")
        print(f"Website being used at {new_data['Start']}")

    else:
        updateFile(new_data)
        return 'JSON file updated!'
    
    return "Sent New message"


def updateFile(jsonFile):
    with open("data.json") as file1:
        old_data = json.load(file1)
    
    if jsonFile["Day"] in old_data:
        old_data[jsonFile["Day"]][jsonFile["Time"]] = {"Info": jsonFile["Info"], "ID": jsonFile["Session ID"]}
    else:
        old_data[jsonFile["Day"]] = {
            jsonFile["Time"] : {"Info": jsonFile["Info"], "ID": jsonFile["Session ID"]}
        }

    with open('data.json', 'w') as f:
        json.dump(old_data, f)


app.run(host='0.0.0.0', port=5000)
