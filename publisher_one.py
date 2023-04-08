import json
import math
import time
import random
import threading
from datetime import datetime

import paho.mqtt.client as mqtt


def random_generator() -> float:
    return random.gauss(1, 1)


class PublisherOne:

    def __init__(self):
        self.thread = None
        self.client = None

    def run(self):
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883, 60)
        self.thread = threading.Thread(target=self.publish_speed_data)
        self.thread.start()

    def publish_speed_data(self):
        i = 0
        while True:
            new_speed = -30 * (math.cos(math.pi / 45 * i)) + (30 + random_generator())
            if int(new_speed) < 0:
                new_speed = 0
            current_time = datetime.now().strftime('%H:%M:%S')
            current_date = datetime.now().strftime('%Y-%m-%d')
            data = {"publisher": "PublisherOne", "date": current_date, "time": current_time, "speed": int(new_speed)}
            print(data)
            json_data = json.dumps(data)
            self.client.publish("vehicle/speed", payload=json_data)
            i += 1
            time.sleep(1)


if __name__ == "__main__":
    publisher_one = PublisherOne()
    publisher_one.run()
    while True:
        pass
