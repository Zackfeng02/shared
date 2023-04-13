from datetime import datetime
import json
import paho.mqtt.client as mqtt


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
        # split data into two dictionaries
        if json_data_in['publisher'] == 'PublisherOne':
            # pub_one_dic stores all data from publisher one and data_list_pub_one store the latest 15
            self.pub_one_dic[key] = json_data_in
            self.data_list_pub_one.append(json_data_in)
            # data_list_pub_one will only store up to 15 set of values to plot
            if len(self.data_list_pub_one) > 15:
                self.data_list_pub_one = self.data_list_pub_one[1:]
            # Content check
            if self.data_list_pub_one:
                print("Messages received by data_list_pub_one:")
                print(self.data_list_pub_one)
            else:
                print("No messages received by data_list_pub_one:.")
        elif json_data_in['publisher'] == 'PublisherTwo':
            # pub_two_dic stores all data from publisher two and data_list_pub_two store the latest 15
            self.pub_two_dic[key] = json_data_in
            self.data_list_pub_two.append(json_data_in)
            # data_list_pub_two will only store up to 15 set of values to plot
            if len(self.data_list_pub_two) > 15:
                self.data_list_pub_two = self.data_list_pub_two[1:]
            # Content check
            if self.data_list_pub_two:
                print("Messages received by data_list_pub_two:")
                print(self.data_list_pub_two)
            else:
                print("No messages received by data_list_pub_two.")


if __name__ == "__main__":
    subsone = SubscriberOne()
    subsone.run()
    while True:
        pass
