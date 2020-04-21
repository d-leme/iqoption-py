from enum import Enum

class ActiveType(Enum):
    binary_option = 3

class Active():
    def __init__(self, id, description, active_type):
        self.id = id
        self.description = description
        self.type = active_type

actives = [
    Active(1, 'EUR/USD', ActiveType.binary_option),
    Active(78, 'USD/CHF (OTC)', ActiveType.binary_option)
]

def get_active_by_description(desc):
    active = next ((a for a in actives if a.description == desc))
    return active 