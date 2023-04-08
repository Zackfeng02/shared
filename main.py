import threading
import time
from publisher_one import PublisherOne
from publisher_two import PublisherTwo
from publisher_three import PublisherThree
from subscriber_one import SubscriberOne
from subscriber_two import SubscriberTwo
from broker import Broker


if __name__ == '__main__':
    # Create an instance of the broker
    broker = Broker()

    # Start the broker
    broker.run()

    # Wait for broker to start
    time.sleep(1)

    # Start publishers
    pub_one = PublisherOne()
    pub_one.run()
    pub_two = PublisherTwo()
    pub_two.run()
    pub_three = PublisherThree()
    pub_three.run()

    # Start subscriber one in a separate thread
    sub_one = SubscriberOne()
    sub_one.run()

    # Start subscriber two
    sub_two = SubscriberTwo()
    sub_two.run()
