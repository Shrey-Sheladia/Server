import os
import json
# import jsonify
import telebot
import threading
from datetime import datetime
from flask import Flask, request
from flask import jsonify



try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

API_KEY = os.environ.get("telegrambotAPI_key")
CHAT_ID = os.environ.get("CHAT_ID")

bot1 = telebot.TeleBot(API_KEY)

app = Flask(__name__)


def createText(last=5):
    with open("data.json") as file1:
        log_data = json.load(file1)
    now = datetime.now()
    day = now.strftime('%d/%m/%Y')

    if day in log_data:
        day_data = log_data[day]
    else:
        day_data = log_data[(list(log_data.keys()))[-1]]

    day_data = dict(list(day_data.items())[-last:])

    str2send = ""

    for time in day_data:
        str2send += f"{time}\n{day_data[time]['ID']}\n{day_data[time]['Info']}\n\n"
    

    return str2send

  
@bot1.message_handler(commands=['get_file'])
def send_log_file(message):
    log_file_path = "data.json"
    if os.path.exists(log_file_path):
        with open(log_file_path, "rb") as log_file:
            bot1.send_document(chat_id=CHAT_ID, document=log_file, caption="data.json")
            print("Sent File")
    else:
        bot1.reply_to(message, "data.json file not found")


@bot1.message_handler(commands=['get_lines'])
def send_lines(message):
    # Get the number of lines to return, default to 5
    try:
        num_lines = int(message.text.split()[1])
    except IndexError:
        num_lines = 5

    str2send = createText(num_lines)
    bot1.send_message(CHAT_ID, str2send)
    print("Sent Lines")


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




### Topic List

@app.route('/get_list_data')
def get_list_data():
    # Load the actualNames.json file and return it as a response
    with open('actualNames.json', 'r') as f:
        actualNames = json.load(f)
    # Load the topic_and_count.json file and return it as a response
    with open('topic_and_count.json', 'r') as f:
        topic_and_count = json.load(f)
    return jsonify({
        'actualNames': actualNames,
        'topicAndCount': topic_and_count
    })

@app.route('/change_list_data', methods=['POST'])
def topic_update():
    new_data = json.loads(request.get_data())
    data = new_data

    actualNames = data['actualNames']
    topic_and_count = data['topicAndCount']

    with open('actualNames.json', 'w') as f:
            json.dump(actualNames, f)
    with open('topic_and_count.json', 'w') as f:
        json.dump(topic_and_count, f)

    return "Files Updated"


    



app.run(host='0.0.0.0', port=5000)
