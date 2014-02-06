# -*- coding: utf-8 -*-
import io
import socket
import redis
import hiredis
from tornado.iostream import IOStream
from .base import PubSubBase

class RedisPubSub(PubSubBase):
    
    def __init__(self, host='127.0.0.1', port=6379, *args, **kwargs):
        self.host = host
        self.port = port
        super(RedisPubSub, self).__init__(*args, **kwargs)

    @staticmethod
    def get_redis():
        return redis.StrictRedis(
            host = '127.0.0.1',
            port = 6379,
            db   = 0
        )

    ##
    ## pubsub api
    ##

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream = IOStream(self.socket)
        self.stream.connect((self.host, self.port), self.on_connect)

    def disconnect(self):
        self.unsubscribe()
        self.stream.close()

    def subscribe(self, channel_id):
        self.send('SUBSCRIBE', channel_id)

    def unsubscribe(self, channel_id=None):
        if channel_id:
            self.send('UNSUBSCRIBE', channel_id)
        else:
            self.send('UNSUBSCRIBE')

    @staticmethod
    def publish(channel_id, message):
        r = RedisPubSub.get_redis()
        r.publish(channel_id, message)

    ##
    ## socket/stream callbacks
    ##

    def on_connect(self):
        self.stream.set_close_callback(self.on_close)
        self.stream.read_until_close(self.on_data, self.on_streaming_data)
        self.reader = hiredis.Reader()
        self.connected()

    def on_data(self, *args, **kwargs):
        pass

    def on_streaming_data(self, data):
        self.reader.feed(data)
        reply = self.reader.gets()
        while reply:
            if reply[0] == 'subscribe':
                self.subscribed(reply[1])
            elif reply[0] == 'unsubscribe':
                self.unsubscribed(reply[1])
            elif reply[0] == 'message':
                self.on_message(reply[1], reply[2])
            else:
                raise Exception('Unhandled data from redis %s' % reply)
            reply = self.reader.gets()

    def on_close(self):
        self.socket = None
        self.stream = None
        self.disconnected()

    ##
    ## redis protocol parser (derived from redis-py)
    ##

    def encode(self, value):
        if isinstance(value, bytes):
            return value
        if isinstance(value, float):
            value = repr(value)
        if not isinstance(value, basestring):
            value = str(value)
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'strict')
        return value

    def pack_command(self, *args):
        cmd = io.BytesIO()
        cmd.write('*')
        cmd.write(str(len(args)))
        cmd.write('\r\n')
        for arg in args:
            arg = self.encode(arg)
            cmd.write('$')
            cmd.write(str(len(arg)))
            cmd.write('\r\n')
            cmd.write(arg)
            cmd.write('\r\n')
        return cmd.getvalue()

    def send(self, *args):
        """Send redis command."""
        cmd = self.pack_command(*args)
        self.stream.write(cmd)
