import messages
import actives

class BollingerBandsStrategy():
    def __init__(self, dispatcher, store):
        self.__configure_handlers(dispatcher, store)

    def __configure_handlers(self, dispatcher, store):
        timeSyncHandler = TimeSyncMessageHandler(dispatcher, store)
        connectionClosedHandler = ConnectionClosedMessageHandler(dispatcher, store)
        subscribeCandleGeneratedHandler = SubscribeCandleGeneratedMessageHandler(dispatcher, store)
        connectionOpennedHandler = ConnectionOpennedMessageHandler(dispatcher, store)
        handlers = [timeSyncHandler, connectionClosedHandler, subscribeCandleGeneratedHandler, connectionOpennedHandler]
        self.handlers = handlers

class TimeSyncMessageHandler():
    def __init__(self, dispatcher, store):
        self.dispatcher = dispatcher
        self.store = store
        self.message_key = "timeSync"

    def handle(self, message):
        pass


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
        self.store.start_operation(active.id)
        

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
        candle = message["msg"]
        active_id = candle["active_id"]
        is_new_candle = self.store.update_candle(active_id, candle)

        if(is_new_candle):
            print("New candle generated")


def get_boilerbands(candles):
    low = 1
    med = 2
    high = 3

    return (low,med,high)
