import sys
from async_pubsub.zmq_pubsub import ZMQPubSub

if __name__ == '__main__':
    channel_id = sys.argv[1]
    message = sys.argv[2]
    ZMQPubSub.publish(channel_id, message)
