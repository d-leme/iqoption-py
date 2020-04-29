import sys
import websocket
import time
import simplejson as json
import _thread as thread
from store import Store
import actives
import messages
from messages import MessageDispatcher
from boilerbands_strategy import BoilerBandsStrategy
from iqoption import Client

user_id = 54515967
real_balance_id = 264298307
practice_balance_id = 264298308

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

def hold_context():
    while True:
        try:
            pass
        except KeyboardInterrupt:
            print('Shutdown requested...exiting')
            return


if __name__ == "__main__":

    # TODO: add logging
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://iqoption.com/echo/websocket")

    dispatcher = MessageDispatcher(ws)
    store = Store()
    store.set_ssid('7183f6a9f2ea4555c71a7fabcc0f9cfc')

    strategy = BoilerBandsStrategy(dispatcher, store)

    client = Client(ws, [strategy])
    client.run_in_background()

    hold_context()

    # TODO: fix exception when trying send message with connection is closed 
    client.close()
    sys.exit(0)
