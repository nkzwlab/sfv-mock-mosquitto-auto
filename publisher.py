import os, json, time, random
import paho.mqtt.client as mqtt
from threading import Thread

BROKER_HOST = os.getenv("MQTT_HOST", "mosquitto")
BROKER_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("PUBLISHER_USER")
MQTT_PASS = os.getenv("PUBLISHER_PASSWORD")

def publish_loop(cfg):
    topic = cfg["topic"]
    msgs  = cfg["message"]
    mode  = cfg.get("type", "random")
    interval = cfg["send_interval"] / 1000.0

    client = mqtt.Client()
    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(BROKER_HOST, BROKER_PORT)

    idx = 0
    while True:
        if mode == "sequential":
            msg = msgs[idx % len(msgs)]
            idx += 1
        else:
            msg = random.choice(msgs)
        client.publish(topic, msg)
        time.sleep(interval)

def main():
    threads = []
    for fname in os.listdir("requests"):
        if not fname.endswith(".json"): continue
        with open(f"requests/{fname}", encoding="utf-8") as f:
            cfg = json.load(f)
        t = Thread(target=publish_loop, args=(cfg,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads: t.join()

if __name__ == "__main__":
    main()
