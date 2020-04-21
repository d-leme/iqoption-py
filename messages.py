import time
import _thread as thread
import simplejson as json

def profile(ssid):
    # TODO: generate ramdom number after underscore
    request_id = f'{int(time.time())}_1071537168'

    return json.dumps({"name": "ssid", "request_id": request_id, "msg": ssid})


def subscribe_candles(request_id, active_id, size):
    return json.dumps({"name": "subscribeMessage", "request_id": f's_{request_id}', "msg": {"name": "candle-generated", "params": {"routingFilters": {"active_id": active_id, "size": size}}}})


def subscribe_active_callback(request_id, active, expires):
    return json.dumps({"name":"subscribeMessage","request_id":"s_202","msg":{"name":"spot-buyback-quote-generated","version":"1.0","params":{"routingFilters":{"active":1,"underlying":"EURUSD","timestamp":expires}}}})


def get_balance(request_id, type_ids):
    return json.dumps({"name": "sendMessage", "request_id": request_id, "msg": {"name": "get-balances", "version": "1.0", "body": {"types_ids": type_ids}}})


def call(request_id, balance_id, active_id, option_type, expire, value, profit_percent):
    return json.dumps({"name": "sendMessage", "request_id": request_id, "msg": {"name": "binary-options.open-option", "version": "1.0", "body": {"user_balance_id": balance_id, "active_id": active_id, "option_type_id": option_type, "direction": "call", "expired": expire, "refund_value": 0, "price": 1.0, "value": value, "profit_percent": profit_percent}}})


def put(request_id, balance_id, active_id, option_type, expire, value, profit_percent):
    return json.dumps({"name": "sendMessage", "request_id": request_id, "msg": {"name": "binary-options.open-option", "version": "1.0", "body": {"user_balance_id": balance_id, "active_id": active_id, "option_type_id": option_type, "direction": "put", "expired": expire, "refund_value": 0, "price": 1.0, "value": value, "profit_percent": profit_percent}}})


def heartbeat(request_id):
    return json.dumps({"name": "heartbeat", "request_id": request_id, "msg": {"userTime": int(time.time()), "heartbeatTime": int(time.time())}})


class MessageDispatcher():
    def __init__(self, conn):
        self.conn = conn

    def dispatch(self, message):
        self.conn.send(message)

    def sleep_then_dispatch(self, message, in_sec):
        time.sleep(in_sec)
        self.dispatch(message)


    def dispatch_every(self, get_message_fn, every_sec):
        def run_in_background():
            while True:
                time.sleep(every_sec)
                self.dispatch(get_message_fn())

        thread.start_new_thread(run_in_background, ())
