import websocket
import time
import simplejson as json
import _thread as thread
import messages
import actives

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

    print("\n" + message + "\n")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")

def heartbeat(ws):
    pass
    # while True:
    #     time.sleep(1)
    #     ws.send(messages.heartbeat(messages.next_count()))


headers = {
    'Pragma': 'no-cache',
    'Origin': 'https://iqoption.com',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Sec-WebSocket-Key': 'IOyTGHyoyoq+9D4xKR6Y6Q==',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Upgrade': 'websocket',
    'Cache-Control': 'no-cache',
    'Cookie': '_ga=GA1.2.372272380.1574015742; _ym_d=1574015744; _ym_uid=1574015744754354880; pll_language=en; ssid=7183f6a9f2ea4555c71a7fabcc0f9cfc; referrer=https://www.google.com/; landing=iqoption.com; identity=901b317a53bee6beeee02271bce03cbf5901cff560e12569d273b252ee798ce14bc5e9caca31915d3c1c3ce982bef395270bedd59a8408e07edcb6ad1b024201025851a073e95203b8776bff3f8619a6f762342f951c59eb6038b0920f0a14e53510e2db9c6d1a685dc48d85b878245275a5c4a3619782fa3f49464f0d84f665536d2fa1ae20d0200831ff4e3aad6d9c272da0bd9115d8e9e3d2689c8d862bebae7bbfa37af986cb19cf02bd11b27500f32ab591465630e13d755b4816b7b5da; lang=en_US; _gid=GA1.2.940076778.1586613076; init_url=https://iqoption.com/en; __uat=c9c64e071d2853bc7906c017a231ad1cc46ab630; device_id=186f7b952656e3ba6facdaf51dbbc3d2; _ym_isad=1; _uetsid=_uetf7583f62-169b-df0a-41b2-90d1f2c9cf53; _gat_UA-44367767-1=1; _ym_visorc_22669009=b; _gat=1; _gat_tracker=1; platform=9; platform_version=1752.2.9413.release',
    'Connection': 'Upgrade',
    'Sec-WebSocket-Version': '13'
}


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://iqoption.com/echo/websocket",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header=headers)

    thread.start_new_thread(ws.run_forever, ())
    time.sleep(1)

    ws.send(messages.profile(ssid))

    time.sleep(1)

    thread.start_new_thread(heartbeat, (ws,))

    active = actives.get_active_by_description('EUR/USD')
    ws.send(messages.subscribe_candles(messages.next_count(), active['id'], 5))

    time.sleep(1)
    ws.send(json.dumps({"name":"sendMessage","request_id":"15","msg":{"name":"register-token","version":"1.0","body":{"app_id":9,"provider":"google","token":"dpfJDY4XH7E:APA91bFf1X1kQ8JuQgsnWhEUOD5T4PnHpukNtvgazj_tcGkpIynNgMl408FrN4Vb-jrqa7BnZBvlsU_EVuGg0YYW5BjYokoCKI14MjIY0sC8nEgIxLj3bo4mqliO3uiqfsesEy-RQ2dN"}}}))
    time.sleep(1)

    ws.send(messages.get_balance(
        messages.next_count(), [account_types['real'], account_types['practice']]))

    input('')
    t_list = list(time.gmtime(int(curr_time / 1000)))
    t_list[3] = t_list[3] - 3
    t_list[4] = t_list[4] + 2
    t_list[5] = 0
    t_list[6] = 0
    t_list[7] = 0
    t_list[8] = 0
    t = int(time.mktime(tuple(t_list)))

    call = messages.call(f'{messages.next_count()}', balances['practice'], active['id'], active['type'], t, int(curr_value * 1000000), 60)
    print(f'Call {call}')

    ws.send(call)
    
    input('')

    ws.close()

