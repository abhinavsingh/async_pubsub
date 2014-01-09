import sys
from async_pubsub import RedisPubSub

if __name__ == '__main__':
    channel_id = sys.argv[1]
    message = sys.argv[2]
    RedisPubSub.publish(channel_id, message)
