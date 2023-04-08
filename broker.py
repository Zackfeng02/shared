import json
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
        json_data_decode = str(message.payload.decode("utf-8"))
        json_data_in = json.loads(json_data_decode)
        print("brk received:")
        print(json_data_in)
        if json_data_in['publisher'] == 'PublisherOne':
            data = {"publisher": "PublisherOne", "date": json_data_in['date'], "time": json_data_in['time'],
                    "speed": json_data_in['speed']}
            new_data = json.dumps(data)
            client.publish("vehicle/speed-filtered-1", payload=new_data)
            print("pub_one data published to vehicle/speed-filtered-1:")
            print(new_data)
            client.publish("vehicle/speed-filtered-2", payload=new_data)
            print("pub_one data published to vehicle/speed-filtered-2:")
            print(new_data)
        elif json_data_in['publisher'] == 'PublisherTwo':
            data = {"publisher": "PublisherTwo", "date": json_data_in['date'], "time": json_data_in['time'],
                    "speed": json_data_in['speed']}
            new_data = json.dumps(data)
            client.publish("vehicle/speed-filtered-1", payload=new_data)
            print("pub_two data published to vehicle/speed-filtered-1:")
            print(new_data)
        elif json_data_in['publisher'] == 'PublisherThree':
            data = {"publisher": "PublisherThree", "date": json_data_in['date'], "time": json_data_in['time'],
                    "speed": json_data_in['speed']}
            new_data = json.dumps(data)
            client.publish("vehicle/speed-filtered-2", payload=new_data)
            print("pub_three data published to vehicle/speed-filtered-2:")
            print(new_data)


if __name__ == "__main__":
    broker = Broker()
    broker.run()
    while True:
        pass
