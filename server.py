from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():
    new_data = json.loads(request.get_json())

    updateFile(new_data)
    return 'JSON file updated!'


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
