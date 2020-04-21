import messages
import actives

class TimeSyncMessageHandler():
    def __init__(self, dispatcher, store):
        self.dispatcher = dispatcher
        self.store = store
        self.message_key = "timeSync"

    def handle(self, message):
        print("time syncronized")


class ConnectionOpennedMessageHandler():
    def __init__(self, dispatcher, store):
        self.dispatcher = dispatcher
        self.store = store
        self.message_key = "connection-openned"

    def handle(self, message):
        profile_message = messages.profile(self.store.ssid)
        self.dispatcher.sleep_then_dispatch(profile_message, 1)

        heartbeat_message = lambda : messages.heartbeat(self.store.next_request_id())
        self.dispatcher.dispatch_every(heartbeat_message, 1)

        active = actives.get_active_by_description('EUR/USD')
        subscribe_candles_message = messages.subscribe_candles(self.store.next_request_id(), active.id, 5)
        self.dispatcher.sleep_then_dispatch(subscribe_candles_message, 1)
        

class ConnectionClosedMessageHandler():
    def __init__(self, dispatcher, store):
        self.dispatcher = dispatcher
        self.store = store
        self.message_key = "connection-closed"

    def handle(self, message):
        print("connection closed")


class SubscribeCandleGeneratedMessageHandler():
    def __init__(self, dispatcher, store):
        self.dispatcher = dispatcher
        self.store = store
        self.message_key = "candle-generated"

    def handle(self, message):
        print("Candle generated")

