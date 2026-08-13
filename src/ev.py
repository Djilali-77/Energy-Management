class Ev:
    def __init__(self, soc, arrival_hour, departure_hour):

        self.battery_capacity = 60
        self.soc = soc
        self.soc_min = 60 
        self.SOC_target = 80
        self.max_charge_power = 7
        self.arrival_hour = arrival_hour
        self.departure_hour = departure_hour

    def charge(self, hour, pv, load):
        stored_energy =  self.soc / 100 * self.battery_capacity

        if self.arrival_hour <= hour < self.departure_hour:
            if self.soc < self.SOC_target:
                charge = pv - load
                if charge < self.max_charge_power:
                    self.soc = stored_energy + charge
                    self.soc =  100/self.battery_capacity * self.soc 
                else:
                    self.soc = stored_energy + self.max_charge_power 
                    self.soc =  100/self.battery_capacity * self.soc
 