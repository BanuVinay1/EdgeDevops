import time
import json
from azure.iot.device import IoTHubModuleClient, Message
from edge_impulse_linux.runner import ImpulseRunner

MODEL_PATH = '/app/model.eim'
client = IoTHubModuleClient.create_from_edge_environment()
client.connect()

def predict_with_model(runner, features):
    result = runner.classify(features)
    return result

def parse_prediction(result):
    predictions = result['result']['classification']
    
    anomaly_score = predictions.get("anomaly", 0)
    print(f"🔍 Anomaly score: {anomaly_score}", flush=True)
    return anomaly_score > 0.5  
def message_handler(message):
    try:
        data = json.loads(message.data)
        print(f"📥 RECEIVED in predictor: {data}", flush=True)

        features = list(data.values())  # assumes {'temperature': 67.5}
        result = predict_with_model(runner, features)
        anomaly_score = result['result']['classification'].get("anomaly", 0)

        print(f"🔍 Anomaly score: {anomaly_score}", flush=True)

        if anomaly_score > 0.5:  # adjust threshold as needed
            print("🚨 Anomaly detected!", flush=True)
            msg = Message(json.dumps({
                "input": data,
                "prediction": "anomaly",
                "score": anomaly_score
            }))
            client.send_message_to_output(msg, "output1")
            print("📤 Sent to IoT Hub", flush=True)
        else:
            print("✅ Normal - not sending", flush=True)

    except Exception as e:
        print(f"❌ Error in handler: {e}", flush=True)

if __name__ == "__main__":
    print("🚀 Starting predictor module", flush=True)

    try:
        runner = ImpulseRunner(MODEL_PATH)
        runner.init()
        print("✅ Model loaded", flush=True)
    except Exception as e:
        print(f"❌ Failed to load model: {str(e)}", flush=True)
        exit(1)

    client.on_message_received = message_handler
    print("✅ Predictor is listening for input...", flush=True)

    while True:
        time.sleep(10)
