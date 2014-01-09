# -*- coding: utf-8 -*-
from .constants import (CALLBACK_TYPE_CONNECTED, CALLBACK_TYPE_SUBSCRIBED,
                        CALLBACK_TYPE_UNSUBSCRIBED, CALLBACK_TYPE_MESSAGE,
                        CALLBACK_TYPE_DISCONNECTED)

class PubSubBase(object):
    
    def __init__(self, callback=None):
        self.callback = callback
    
    ##
    ## Methods implementation must define
    ##
    
    def connect(self):
        raise NotImplementedError()
    
    def disconnect(self):
        raise NotImplementedError()
    
    def subscribe(self):
        raise NotImplementedError()
    
    def unsubscribe(self):
        raise NotImplementedError()
    
    @staticmethod
    def publish(channel_id, message):
        raise NotImplementedError()
    
    ## 
    ## events implementation must emit
    ## user callback is appropriately called
    ## 
    
    def connected(self):
        self.callback(CALLBACK_TYPE_CONNECTED)
    
    def disconnected(self):
        self.callback(CALLBACK_TYPE_DISCONNECTED)
    
    def subscribed(self, channel_id):
        self.callback(CALLBACK_TYPE_SUBSCRIBED, channel_id)
    
    def unsubscribed(self, channel_id):
        self.callback(CALLBACK_TYPE_UNSUBSCRIBED, channel_id)
    
    def on_message(self, channel_id, message):
        self.callback(CALLBACK_TYPE_MESSAGE, channel_id, message)
