class Battery:
    def __init__(self, soc):

        self.capacity = 40
        self.soc = soc
        self.max_charge_power = 5
        self.max_discharge_power = 5
        self.efficiency = 0.9
        self.soc_min = 20
        self.soc_max = 90

    def charge(self, solar, demande):

        surplus = solar - demande

        if surplus <= 0 or self.soc >= self.soc_max:
            return 0

        stored_energy = self.soc / 100 * self.capacity
        remaining = self.capacity * self.soc_max / 100 - stored_energy

        charge_power = min(surplus, self.max_charge_power)

        energy_stored = charge_power * self.efficiency

        energy_stored = min(energy_stored, remaining)

        self.soc = (stored_energy + energy_stored) / self.capacity * 100

        return energy_stored


    def discharge(self, solar, demande):

        deficit = demande - solar

        if deficit <= 0 or self.soc <= self.soc_min:
            return 0

        stored_energy = self.soc / 100 * self.capacity
        minimum_energy = self.capacity * self.soc_min / 100

        available = stored_energy - minimum_energy

        discharge_power = min(deficit, self.max_discharge_power)

        energy_needed_from_battery = discharge_power / self.efficiency

        if energy_needed_from_battery > available:
            energy_needed_from_battery = available

        energy_delivered = energy_needed_from_battery * self.efficiency

        self.soc = (stored_energy - energy_needed_from_battery) / self.capacity * 100

        return energy_delivered