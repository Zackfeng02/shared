import json
import logging

import paho.mqtt.client as mqtt


class Broker:
    def __init__(self):
        self.thread = None
        self.client = None
        self.messages = []

    def run(self):
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("vehicle/speed")

    def on_message(self, client, userdata, message):
        try:
            json_data_in = json.loads(message.payload.decode())
            publisher = json_data_in['publisher']
            date = json_data_in['date']
            time = json_data_in['time']
            speed = json_data_in['speed']
            if publisher == 'PublisherOne':
                data_one = {"publisher": publisher, "date": date, "time": time,
                            "speed": speed}
                new_data = json.dumps(data_one)
                client.publish("vehicle/speed-filtered-1", payload=new_data)
                print("pub_one data published to vehicle/speed-filtered-1:")
                print(new_data)
                client.publish("vehicle/speed-filtered-2", payload=new_data)
                print("pub_one data published to vehicle/speed-filtered-2:")
                print(new_data)
            elif publisher == 'PublisherTwo':
                data_two = {"publisher": publisher, "date": date, "time": time,
                            "speed": speed}
                new_data = json.dumps(data_two)
                client.publish("vehicle/speed-filtered-1", payload=new_data)
                print("pub_two data published to vehicle/speed-filtered-1:")
                print(new_data)
            elif publisher == 'PublisherThree':
                data_three = {"publisher": publisher, "date": date, "time": time,
                              "speed": speed}
                new_data = json.dumps(data_three)
                client.publish("vehicle/speed-filtered-2", payload=new_data)
                print("pub_three data published to vehicle/speed-filtered-2:")
                print(new_data)
        except (json.JSONDecodeError, KeyError):
            logging.error("Error decoding message payload: %s", message.payload)
        except TypeError:
            logging.info("Received message payload as str: %s", message.payload)


if __name__ == "__main__":
    broker = Broker()
    broker.run()
    while True:
        pass
