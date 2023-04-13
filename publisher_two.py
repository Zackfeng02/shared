import json
import math
import string
import time
import random
import threading
from datetime import datetime

import paho.mqtt.client as mqtt


def random_generator() -> float:
    return random.gauss(1, 1)


class PublisherTwo:

    def __init__(self):
        self.thread = None
        self.client = None
        self.data_buffer = {}

    def run(self):
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883, 60)
        self.thread = threading.Thread(target=self.publish_speed_data)
        self.thread.start()

    def buffer_data(self, data):
        self.data_buffer = json.dumps(data)
        print("Communication error, buffer created.")

    def publish_data(self, data):
        json_data = json.dumps(data)
        self.client.publish("vehicle/speed", payload=json_data)
        print(data)

    def publish_buffer(self):
        json_buffer = json.dumps(self.data_buffer)
        self.client.publish("vehicle/speed", payload=json_buffer)
        print("Buffer data is sent successfully!")
        self.data_buffer = {}

    def publish_speed_data(self):
        iteration_count = 0
        while True:
            new_speed = -50 * (math.cos(math.pi / 40 * iteration_count)) + (50 + random_generator())
            if int(new_speed) < 0:
                new_speed = 0
            current_time = datetime.now().strftime('%H:%M:%S')
            current_date = datetime.now().strftime('%Y-%m-%d')
            data = {"publisher": "PublisherTwo", "date": current_date, "time": current_time,
                    "speed": int(new_speed)}

            # Generate a random number between 0 and 1
            rand_num = random.random()

            if rand_num < 0.01:
                # Store the data in the buffer first
                self.buffer_data(data)
                data = {}
            else:
                # Send the buffer data first if it exists, then the new data
                if self.data_buffer:
                    # Send out buffer first
                    self.publish_buffer()
                    # Then send out new data
                    self.publish_data(data)
                else:
                    # Decide if the data is corrupted
                    wild_data = ""
                    rand_num = random.random()
                    if rand_num < 0.005:
                        # Mutate data to a 10 digit random string
                        wild_data = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                        json_wild = json.dumps(wild_data)
                        self.client.publish("vehicle/speed", payload=json_wild)
                        print("Corrupted data published:" + wild_data)
                    else:
                        self.publish_data(data)

            iteration_count += 1
            time.sleep(1)


if __name__ == "__main__":
    publisher_two = PublisherTwo()
    publisher_two.run()
    while True:
        pass
