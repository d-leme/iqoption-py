actives = [
    {
        'id': 78,
        'description' : 'USD/CHF (OTC)',
        'type': 3
    }
]

def get_active_by_description(desc):
    active = next ((a for a in actives if a['description'] == desc))
    return active 