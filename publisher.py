import os, json, time, random
import paho.mqtt.client as mqtt
from threading import Thread

BROKER_HOST = os.getenv("MQTT_HOST", "mosquitto")
BROKER_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("PUBLISHER_USER")
MQTT_PASS = os.getenv("PUBLISHER_PASSWORD")

def get_message_content(msg):
    if isinstance(msg, str) and msg.startswith("file:"):
        file_path = msg[5:]  # "file:"を除去
        
        # パストラバーサル攻撃を防ぐサニタイゼーション
        # "../"や"..\\"などの危険なパスを無効化
        if ".." in file_path or file_path.startswith("/") or "\\" in file_path:
            raise ValueError(f"Invalid file path: {file_path}")
        
        # reffile以下のパスとして解釈
        full_path = os.path.join("reffile", file_path)
        
        # 正規化してreffileディレクトリ外へのアクセスを防ぐ
        normalized_path = os.path.normpath(full_path)
        if not normalized_path.startswith(os.path.normpath("reffile")):
            raise ValueError(f"Path outside reffile directory: {file_path}")
        
        with open(normalized_path, 'r', encoding='utf-8') as f:
            return f.read()
    return msg

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
        
        # ファイル参照の場合は内容を読み込む
        content = get_message_content(msg)
        client.publish(topic, content)
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
