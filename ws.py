import websocket
import time
import simplejson as json
import _thread as thread
import messages
import actives
from store import Store

user_id = 54515967
real_balance_id = 264298307
practice_balance_id = 264298308
ssid = '7183f6a9f2ea4555c71a7fabcc0f9cfc'

balances = {
    'real': 264298307,
    'practice': 264298308
}

account_types = {
    'real': 1,
    'practice': 4
}

real_account_type = 1
practice_account_type = 4

curr_time = 0
curr_value = 0
store = Store()

def on_message(ws, message):
    message_obj = json.loads(message)

    if message_obj['name'] == 'timeSync':
        global curr_time
        curr_time = message_obj['msg']

    if message_obj['name'] == 'candle-generated':
        global curr_value
        curr_value = message_obj['msg']['ask']

    if message_obj['name'] == 'timeSync' or message_obj['name'] == 'heartbeat':
        return

    if(message_obj['name'] == "socket-option-closed"):
        print("\n\nOption closed\n")
        print(message)
        print("\n")
        ws.close()

    print("\n" + message + "\n")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")

def heartbeat(ws):
    while True:
        time.sleep(1)
        ws.send(messages.heartbeat(store.next_request_id()))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://iqoption.com/echo/websocket",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    thread.start_new_thread(ws.run_forever, ())
    time.sleep(1)

    ws.send(messages.profile(ssid))

    time.sleep(1)

    thread.start_new_thread(heartbeat, (ws,))

    active = actives.get_active_by_description('EUR/USD')
    ws.send(messages.subscribe_candles(store.next_request_id(), active.id, 5))

    time.sleep(1)
    ws.send(json.dumps({"name":"sendMessage","request_id":"15","msg":{"name":"register-token","version":"1.0","body":{"app_id":9,"provider":"google","token":"dpfJDY4XH7E:APA91bFf1X1kQ8JuQgsnWhEUOD5T4PnHpukNtvgazj_tcGkpIynNgMl408FrN4Vb-jrqa7BnZBvlsU_EVuGg0YYW5BjYokoCKI14MjIY0sC8nEgIxLj3bo4mqliO3uiqfsesEy-RQ2dN"}}}))
    time.sleep(1)

    ws.send(messages.get_balance(
        store.next_request_id(), [account_types['real'], account_types['practice']]))

    input('')
    t_list = list(time.gmtime(int(curr_time / 1000)))
    t_list[3] = t_list[3] - 3
    t_list[4] = t_list[4] + 2
    t_list[5] = 0
    t_list[6] = 0
    t_list[7] = 0
    t_list[8] = 0
    t = int(time.mktime(tuple(t_list)))

    call_msg = messages.call(f'{store.next_request_id()}', balances['practice'], active.id, active.type.value, t, int(curr_value * 1000000), 57)
    ws.send(call_msg)
    
    time.sleep(.05)
    callback_msg = messages.subscribe_active_callback(f'{store.next_request_id()}', active.id, t)

    
    input('')

    ws.close()

