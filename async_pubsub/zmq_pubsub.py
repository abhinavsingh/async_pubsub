# -*- coding: utf-8 -*-
import zmq
from zmq.eventloop.zmqstream import ZMQStream
import logging
from .base import PubSubBase

logger = logging.getLogger(__name__)

class ZMQPubSub(PubSubBase):
    
    def __init__(self, device_ip='127.0.0.1', fport=5559, bport=5560, *args, **kwargs):
        self.channels = list()
        self.device_ip = '127.0.0.1'
        self.fport = fport
        self.bport = bport
        super(ZMQPubSub, self).__init__(*args, **kwargs)

    ##
    ## pubsub api
    ##
    
    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://%s:%s' % (self.device_ip, self.bport))
        self.stream = ZMQStream(self.socket)
        self.stream.on_recv(self.on_streaming_data)
        self.connected()

    def disconnect(self):
        self.disconnected()

    def subscribe(self, channel_id):
        self.socket.setsockopt(zmq.SUBSCRIBE, str(channel_id))
        self.channels.append(channel_id)
        self.subscribed(channel_id)

    def unsubscribe(self, channel_id=None):
        channels = [channel_id] if channel_id else self.channels
        for channel_id in channels:
            self.socket.setsockopt(zmq.UNSUBSCRIBE, str(channel_id))
            self.unsubscribed(channel_id)
            self.channels.remove(channel_id)

    @staticmethod
    def publish(channel_id, message, device_ip='127.0.0.1', fport=5559):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect('tcp://%s:%s' % (device_ip, fport))
        socket.send_unicode('%s %s' % (channel_id, message))

    ##
    ## other methods
    ##
    
    def on_streaming_data(self, data):
        for l in data:
            reply = l.split(' ', 1)
            self.on_message(reply[0], reply[1])

    @staticmethod
    def start_service(fport=5559, bport=5560):
        try:
            context = zmq.Context(1)
            
            frontend = context.socket(zmq.PULL)
            frontend.bind('tcp://*:%s' % fport)
            
            backend = context.socket(zmq.PUB)
            backend.bind('tcp://*:%s' % bport)
            
            logger.info('starting zmq device')
            zmq.device(zmq.FORWARDER, frontend, backend)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.exception(e)
        finally:
            frontend.close()
            backend.close()
            context.term()

