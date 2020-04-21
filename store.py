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
