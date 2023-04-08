import math
import threading
import time
import json
import random
from datetime import datetime

import paho.mqtt.client as mqtt


def random_generator() -> float:
    return random.gauss(1, 1)


class PublisherThree:

    def __init__(self):
        self.client = None
        self.thread = None

    def run(self):
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883, 60)
        self.thread = threading.Thread(target=self.publish_speed_data)
        self.thread.start()

    def publish_speed_data(self):
        i = 0
        while True:
            new_speed = -40 * (math.cos(math.pi / 35 * i)) + (40 + random_generator())
            if int(new_speed) < 0:
                new_speed = 0
            current_time = datetime.now().strftime('%H:%M:%S')
            current_date = datetime.now().strftime('%Y-%m-%d')
            data = {"publisher": "PublisherThree", "date": current_date, "time": current_time, "speed": int(new_speed)}
            print(data)
            json_data = json.dumps(data)
            self.client.publish("vehicle/speed", payload=json_data)
            i += 1
            time.sleep(1)


if __name__ == "__main__":
    publisher_three = PublisherThree()
    publisher_three.run()
    while True:
        pass
