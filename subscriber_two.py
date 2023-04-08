import json
import time
import paho.mqtt.client as mqtt


class SubscriberTwo:
    all_data_dic = {}
    pub_one_dic = {}
    pub_three_dic = {}
    current_speed = 0

    def __init__(self):
        self.thread = None
        self.client = None

    def run(self):
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("vehicle/speed-filtered-2")

    def on_message(self, client, userdata, msg):
        json_data_decode = str(msg.payload.decode("utf-8"))
        json_data_in = json.loads(json_data_decode)
        key = str(time.time())
        self.all_data_dic[key] = json_data_in
        if json_data_in['publisher'] == 'PublisherOne':
            key = str(time.time())
            self.pub_one_dic[key] = json_data_in
        elif json_data_in['publisher'] == 'PublisherThree':
            key = str(time.time())
            self.pub_three_dic[key] = json_data_in
        # Block below is used to check if message is loaded to the dic
        # if SubscriberOne.pub_one_dic:
        # print("Messages received by pub_one_dic:")
        # for key, value in SubscriberOne.pub_one_dic.items():
        # print(key, ":", value)
        # else:
        # print("No messages received by pub_one_dic.")


if __name__ == "__main__":
    substwo = SubscriberTwo()
    substwo.run()
    while True:
        pass
