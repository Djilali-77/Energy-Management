import pandas as pd

data = {
    "hour": list(range(24)),
    "solar_power_kW": [
        0, 0, 0, 0, 0, 0.3,
        1.2, 2.8, 4.5, 6.2, 7.8, 9.0,
        10.0, 9.4, 8.2, 6.5, 4.3, 2.2,
        0.8, 0, 0, 0, 0, 0
    ]
}

class Solar:
    def __init__(self, max_power, data):

        self.max_power = max_power #df['solar_power_kW'].max()
        self.solar_available =  data["solar_power_kW"]

    def get_production(self, hour):
        return self.solar_available[hour]


pv1 = Solar(10, data)
print(pv1.get_production(6))