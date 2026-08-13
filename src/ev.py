class Ev:
    def __init__(self, soc, arrival_hour, departure_hour):

        self.battery_capacity = 60
        self.soc = soc
        self.soc_min = 60
        self.SOC_target = 80
        self.max_charge_power = 7
        self.arrival_hour = arrival_hour
        self.departure_hour = departure_hour

    def charge(self, hour, surplus):

        if self.arrival_hour <= hour < self.departure_hour:

            if self.soc < self.SOC_target:

                stored_energy = self.soc / 100 * self.battery_capacity
                target_energy = self.SOC_target / 100 * self.battery_capacity
                remaining_capacity = target_energy - stored_energy

                charge = min(
                    surplus,
                    self.max_charge_power,
                    remaining_capacity
                )

                self.soc = (stored_energy + charge) / self.battery_capacity * 100

                return charge

        return 0