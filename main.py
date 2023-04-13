import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import threading

from broker import Broker
from publisher_one import PublisherOne
from publisher_two import PublisherTwo
from publisher_three import PublisherThree
from subscriber_one import SubscriberOne
from subscriber_two import SubscriberTwo


class PlotData:

    def __init__(self, master):
        # GUI settings for Subscriber One
        self.master = master
        self.master.title("Subscriber One Data Display")
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

        # GUI settings for Subscriber Two
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Subscriber Two Data Display")
        self.new_fig = Figure(figsize=(10, 5), dpi=100)

        self.new_left_subplot = self.new_fig.add_subplot(121)
        self.new_left_subplot.set_title('Publisher One')
        self.new_left_subplot.set_xlabel('Time')
        self.new_left_subplot.set_ylabel('Speed')
        self.new_left_subplot.set_ylim([0, 60])

        self.new_right_subplot = self.new_fig.add_subplot(122)
        self.new_right_subplot.set_title('Publisher Three')
        self.new_right_subplot.set_xlabel('Time')
        self.new_right_subplot.set_ylabel('Speed')
        self.new_right_subplot.set_ylim([0, 60])

        self.new_canvas = FigureCanvasTkAgg(self.new_fig, self.new_window)
        self.new_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.run()

    def run(self):
        broker = Broker()
        pub_one = PublisherOne()
        pub_two = PublisherTwo()
        pub_three = PublisherThree()
        sub_one = SubscriberOne()
        sub_two = SubscriberTwo()

        t1 = threading.Thread(target=broker.run, daemon=True)
        t2 = threading.Thread(target=pub_one.run, daemon=True)
        t3 = threading.Thread(target=pub_two.run, daemon=True)
        t4 = threading.Thread(target=pub_three.run, daemon=True)
        t5 = threading.Thread(target=sub_one.run, daemon=True)
        t6 = threading.Thread(target=sub_two.run, daemon=True)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

        self.update_plot()

    def update_plot(self):
        # Get data from SubscriberOne
        sub_one = SubscriberOne()
        data_list_pub_one = sub_one.data_list_pub_one
        data_list_pub_two = sub_one.data_list_pub_two

        # Clear the previous plot
        self.left_subplot.clear()
        self.right_subplot.clear()
        self.new_left_subplot.clear()
        self.new_right_subplot.clear()

        # Set the title, x-label, and y-label for the left subplot
        self.left_subplot.set_title('Publisher One')
        self.left_subplot.set_xlabel('Time')
        self.left_subplot.set_ylabel('Speed')

        # Set the title, x-label, and y-label for the right subplot
        self.right_subplot.set_title('Publisher Two')
        self.right_subplot.set_xlabel('Time')
        self.right_subplot.set_ylabel('Speed')

        # Set the title, x-label, and y-label for the new left subplot
        self.new_left_subplot.set_title('Publisher One')
        self.new_left_subplot.set_xlabel('Time')
        self.new_left_subplot.set_ylabel('Speed')

        # Set the title, x-label, and y-label for the new right subplot
        self.new_right_subplot.set_title('Publisher Three')
        self.new_right_subplot.set_xlabel('Time')
        self.new_right_subplot.set_ylabel('Speed')

        # Plot the data for Publisher One from SubscriberOne
        if data_list_pub_one:
            x = []
            y = []
            for data in data_list_pub_one:
                time_pub_one = datetime.strptime(data['time'], '%H:%M:%S')
                if len(x) > 20:
                    x.pop(0)
                if len(y) > 20:
                    y.pop(0)
                x.append(time_pub_one)
                y.append(data['speed'])
            self.left_subplot.plot(x, y, 'bo-')
            self.left_subplot.set_xlim([x[0], x[-1] + timedelta(seconds=1)])

        # Plot the data for Publisher Two from SubscriberOne
        if data_list_pub_two:
            x = []
            y = []
            for data in data_list_pub_two:
                time_pub_two = datetime.strptime(data['time'], '%H:%M:%S')
                if len(x) > 20:
                    x.pop(0)
                if len(y) > 20:
                    y.pop(0)
                x.append(time_pub_two)
                y.append(data['speed'])
            self.right_subplot.plot(x, y, 'ro-')
            self.right_subplot.set_xlim([x[0], x[-1] + timedelta(seconds=1)])

        # Get data from SubscriberTwo
        sub_two = SubscriberTwo()
        data_list_pub_one = sub_two.data_list_pub_one
        data_list_pub_three = sub_two.data_list_pub_three

        # Plot the data for Publisher One from SubscriberTwo
        if data_list_pub_one:
            x = []
            y = []
            for data in data_list_pub_one:
                time_pub_one = datetime.strptime(data['time'], '%H:%M:%S')
                if len(x) > 20:
                    x.pop(0)
                if len(y) > 20:
                    y.pop(0)
                x.append(time_pub_one)
                y.append(data['speed'])
            self.new_left_subplot.plot(x, y, 'bo-')
            self.new_left_subplot.set_xlim([x[0], x[-1] + timedelta(seconds=1)])

        # Plot the data for Publisher Three from SubscriberTwo
        if data_list_pub_three:
            x = []
            y = []
            for data in data_list_pub_three:
                time_pub_three = datetime.strptime(data['time'], '%H:%M:%S')
                if len(x) > 20:
                    x.pop(0)
                if len(y) > 20:
                    y.pop(0)
                x.append(time_pub_three)
                y.append(data['speed'])
            self.new_right_subplot.plot(x, y, 'go-')
            self.new_right_subplot.set_xlim([x[0], x[-1] + timedelta(seconds=1)])

        # Redraw the plots
        self.canvas.draw()
        self.new_canvas.draw()

        # Schedule the next update
        self.master.after(500, self.update_plot)


if __name__ == '__main__':
    root = tk.Tk()
    PlotData(root)
    root.mainloop()
