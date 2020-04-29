class Store():
    def __init__(self):
        self.current_time = 0
        self.request_counter = 0
        self.ssid = ''
        self.operations = []

    def set_time(self, time):
        self.current_time = time

    def set_ssid(self, ssid):
        self.ssid = ssid
    
    def next_request_id(self):
        self.request_counter + 1
        return self.request_counter

    def start_operation(self, active):
        self.operations.append({"active_id": active, "candles": []})

    def update_candle(self, active, candle):
        for op in self.operations:
            found_active = active == op["active_id"]
            found_candle = any(c for c in op["candles"] if c["id"] == candle["id"])

            if found_active and not found_candle:
                op["candles"].append(candle)
                return True
                
        return False
                