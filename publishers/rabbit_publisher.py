#!/usr/bin/env python
import pika
import sys
import logging
import json

from base_publisher import BasePublisher

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)

class RabbitPublisher(BasePublisher):
    def __init__(self, conf):

        self.host = conf["host"]
        self.queue = conf["queue"]

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host))
        
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True)

    def publish(self, message):
        # message = ' '.join(sys.argv[1:]) or "Hello World!"
        message = json.dumps(message, sort_keys=True)
        self.channel.basic_publish(exchange='',
                              routing_key=self.queue,
                              body=message,
                              properties=pika.BasicProperties(
                                 delivery_mode = 2, # make message persistent
                              ))

        # print " [x] Sent %r" % (message,)

    def close(self):
        self.connection.close()



# rp = RabbitPublisher({"host": "127.0.0.1", "queue": "log_queue"})

# rp.publish("message")

# rp.close()
