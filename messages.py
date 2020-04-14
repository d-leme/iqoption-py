import time
import simplejson as json

sent_count = 0


def next_count():
    global sent_count

    nr = sent_count

    sent_count += 1

    return nr


def profile(ssid):
    # TODO: generate ramdom number after underscore
    request_id = f'{int(time.time())}_1071537168'

    return json.dumps({"name": "ssid", "request_id": request_id, "msg": ssid})


def subscribe_candles(request_id, active_id, size):
    return json.dumps({"name": "subscribeMessage", "request_id": f's_{request_id}', "msg": {"name": "candle-generated", "params": {"routingFilters": {"active_id": active_id, "size": size}}}})


def get_balance(request_id, type_ids):
    return json.dumps({"name": "sendMessage", "request_id": request_id, "msg": {"name": "get-balances", "version": "1.0", "body": {"types_ids": type_ids}}})


def call(request_id, balance_id, active_id, option_type, expire, value, profit_percent):
    return json.dumps({"name": "sendMessage", "request_id": request_id, "msg": {"name": "binary-options.open-option", "version": "1.0", "body": {"user_balance_id": balance_id, "active_id": active_id, "option_type_id": option_type, "direction": "call", "expired": expire, "refund_value": 0, "price": 1.0, "value": value, "profit_percent": profit_percent}}})


def put(request_id, balance_id, active_id, option_type, expire, value, profit_percent):
    return json.dumps({"name": "sendMessage", "request_id": request_id, "msg": {"name": "binary-options.open-option", "version": "1.0", "body": {"user_balance_id": balance_id, "active_id": active_id, "option_type_id": option_type, "direction": "put", "expired": expire, "refund_value": 0, "price": 1.0, "value": value, "profit_percent": profit_percent}}})


def heartbeat(request_id):
    return json.dumps({"name": "heartbeat", "request_id": request_id, "msg": {"userTime": int(time.time()), "heartbeatTime": int(time.time())}})
