import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import threading
import time
import json
from typing import List

from broker import Broker
from publisher_one import PublisherOne
from publisher_two import PublisherTwo
from subscriber_one import SubscriberOne


class PlotData:

    def __init__(self, master):
        self.master = master
        self.master.title("Vehicle Speed Data")
        self.fig = Figure(figsize=(10, 5), dpi=100)

        self.left_subplot = self.fig.add_subplot(121)
        self.left_subplot.set_title('Publisher One')
        self.left_subplot.set_xlabel('Time')
        self.left_subplot.set_ylabel('Speed')
        self.left_subplot.set_ylim([0, 60])

        self.right_subplot = self.fig.add_subplot(122)
        self.right_subplot.set_title('Publisher Two')
        self.right_subplot.set_xlabel('Time')
        self.right_subplot.set_ylabel('Speed')
        self.right_subplot.set_ylim([0, 60])

        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.run()

    def run(self):
        broker = Broker()
        pub_one = PublisherOne()
        pub_two = PublisherTwo()
        sub_one = SubscriberOne()

        t1 = threading.Thread(target=broker.run)
        t2 = threading.Thread(target=pub_one.run)
        t3 = threading.Thread(target=pub_two.run)
        t4 = threading.Thread(target=sub_one.run)

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        self.update_plot()

    def update_plot(self):
        # Get data from SubscriberOne
        sub_one = SubscriberOne()
        data_list_pub_one = sub_one.data_list_pub_one
        data_list_pub_two = sub_one.data_list_pub_two

        # Clear the previous plot
        self.left_subplot.clear()
        self.right_subplot.clear()

        # Plot the data for Publisher One
        if data_list_pub_one:
            x = []
            y = []
            for data in data_list_pub_one:
                time_pub_one = datetime.strptime(data['time'], '%H:%M:%S')
                x.append(time_pub_one)
                y.append(data['speed'])
            self.left_subplot.plot(x, y, 'bo-')
            self.left_subplot.set_xlim([x[0], x[-1] + timedelta(seconds=1)])

        # Plot the data for Publisher Two
        if data_list_pub_two:
            x = []
            y = []
            for data in data_list_pub_two:
                time_pub_two = datetime.strptime(data['time'], '%H:%M:%S')
                x.append(time_pub_two)
                y.append(data['speed'])
            self.right_subplot.plot(x, y, 'ro-')
            self.right_subplot.set_xlim([x[0], x[-1] + timedelta(seconds=1)])

        self.canvas.draw()
        self.master.after(500, self.update_plot)


if __name__ == '__main__':
    root = tk.Tk()
    PlotData(root)
    root.mainloop()
