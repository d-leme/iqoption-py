import simplejson as json
import time
import _thread as thread

class Client():
    def __init__(self, conn, strategies):
        self.conn = conn
        self.strategies = strategies

    def __exec_handler(self, message):
        for strategy in self.strategies:
            found_handlers = [
                h for h in strategy.handlers if h.message_key == message['name']]

            for h in found_handlers:
                h.handle(message)

    def _on_message(self):
        return lambda _, message: self.__exec_handler(json.loads(message))

    def _on_open(self):
        return lambda _: self.__exec_handler({"name": 'connection-openned'})

    def _on_close(self):
        return lambda _: self.__exec_handler({"name": 'connection-closed'})

    def _on_error(self):
        return lambda _, error: self.__exec_handler({"name": 'error-occured', "error": error})

    def run_in_background(self):
        self.conn.on_message = self._on_message()
        self.conn.on_open = self._on_open()
        self.conn.on_close = self._on_close()
        self.conn.on_error = self._on_error()

        thread.start_new_thread(self.conn.run_forever, ())

    def close(self):
        self.conn.close()
