import flask
from flask import request, jsonify
import plivo

auth_id = "YOUR_AUTH_ID"
auth_token = "YOUR_AUTH_TOKEN"

app_id = "APP_ID"

target_number = "YOUR_PHONE_NUMBER"


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Plivo SMS API APP</h1><p>This app is a API for reading sms from Plivo.</p>"

@app.route('/api/v1/getSMS', methods=['GET'])
def api_all():
    query_parameters = request.args
    
    number_from = query_parameters.get('number_from')
    number_to = query_parameters.get('number_to')
    msg_body = query_parameters.get('msg_body')

    print("SMS From: ",number_from)
    print("SMS To: ",number_to)
    print("SMS : '",msg_body, "'")

    p = plivo.RestClient(auth_id, auth_token)
    response = p.messages.create(
        src=number_to,
        dst=target_number,
        text= msg_body,
    )
    print(response)

    return jsonify({"status": "success"})

@app.route('/api/v1/number', methods=['GET'])
def api_get_number():
    p = plivo.RestClient(auth_id, auth_token)

    response = p.numbers.search(country_iso='US',type='local',region='texas')

    available_number = str(response.objects[0].number)
    print (available_number)
    response1 = p.numbers.buy(number=available_number,app_id=app_id)
    print (str(response1.numbers))
    return jsonify({"number": str(response1.numbers[0].number), "status": str(response1.numbers[0].status)})

app.run(host="0.0.0.0", port=80)