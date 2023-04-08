import time
from datetime import datetime
import json
import threading
import paho.mqtt.client as mqtt
from matplotlib import pyplot as plt
from matplotlib import dates as mdates


class SubscriberOne:
    all_data_dic = {}
    pub_one_dic = {}
    pub_two_dic = {}
    data_list_pub_one = []
    data_list_pub_two = []
    current_pub_speed = 0

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
        client.subscribe("vehicle/speed-filtered-1")

    def on_message(self, client, userdata, msg):
        json_data_decode = str(msg.payload.decode("utf-8"))
        json_data_in = json.loads(json_data_decode)
        key = str(datetime.now())
        self.all_data_dic[key] = json_data_in
        if json_data_in['publisher'] == 'PublisherOne':
            self.pub_one_dic[key] = json_data_in
            self.data_list_pub_one.append(json_data_in)
        elif json_data_in['publisher'] == 'PublisherTwo':
            self.pub_two_dic[key] = json_data_in
            self.data_list_pub_two.append(json_data_in)


if __name__ == "__main__":
    subsone = SubscriberOne()
    subsone.run

    while True:
        pass
