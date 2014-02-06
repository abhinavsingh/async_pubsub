import sys
from tornado.ioloop import IOLoop

from async_pubsub.zmq_pubsub import ZMQPubSub
from async_pubsub.constants import (CALLBACK_TYPE_CONNECTED, CALLBACK_TYPE_SUBSCRIBED, 
                                    CALLBACK_TYPE_UNSUBSCRIBED, CALLBACK_TYPE_MESSAGE,
                                    CALLBACK_TYPE_DISCONNECTED)

from zmq.eventloop import ioloop as zmq_ioloop
zmq_ioloop.install()

ioloop = IOLoop.instance()

class Subscriber(object):
    
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.r = ZMQPubSub(callback=self.callback)
        self.r.connect()
    
    def callback(self, evtype, *args, **kwargs):
        if evtype == CALLBACK_TYPE_CONNECTED:
            print 'connected'
            self.r.subscribe(self.channel_id)
        elif evtype == CALLBACK_TYPE_SUBSCRIBED:
            print 'subscribed to channel_id %s' % args[0]
        elif evtype == CALLBACK_TYPE_MESSAGE:
            print 'received on channel_id %s message %s' % (args[0], args[1])
            self.r.unsubscribe()
        elif evtype == CALLBACK_TYPE_UNSUBSCRIBED:
            print 'unsubscribed'
            self.r.disconnect()
        elif evtype == CALLBACK_TYPE_DISCONNECTED:
            print 'disconnected'
            ioloop.stop()

if __name__ == '__main__':
    channel_id = sys.argv[1]
    subscriber = Subscriber(channel_id)
    ioloop.start()
    print 'done.'
