import time
import json
import random
from azure.iot.device import IoTHubModuleClient, Message

def generate_temp():
    if random.random() < 0.8:
        return round(random.uniform(30.0, 70.0), 2)
    else:
        return round(random.choice([random.uniform(5.0, 15.0), random.uniform(85.0, 100.0)]), 2)

client = IoTHubModuleClient.create_from_edge_environment()
client.connect()

while True:
    temp = generate_temp()
    payload = { "temperature": temp }
    print("📤 Sending:", payload, flush=True)

    msg = Message(json.dumps(payload))
    client.send_message_to_output(msg, "output1")

    time.sleep(5)
