data = {
    "hour": list(range(24)),
    "demand_kW": [
        1.8, 1.6, 1.5, 1.4, 1.5, 1.8,
        2.5, 3.0, 3.2, 3.0, 2.8, 2.7,
        2.6, 2.5, 2.8, 3.2, 4.0, 4.5,
        5.0, 5.5, 5.8, 5.0, 4.2, 3.0
    ]
}

class Load:
    def __init__(self, data):
        self.demand = data["demand_kW"]

    def get_demand(self, hour):
        return self.demand[hour]