import zmq
import json

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5560")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "jsondata")

while True:
    try:
        message = subscriber.recv_string()
        topic, json_payload = message.split(' ', 1)
        use_pos = json.loads(json_payload)
        print(type(use_pos), use_pos[0], use_pos[1], use_pos[2])
    except:
        topic, json_payload = message
        print(json.loads(json_payload))