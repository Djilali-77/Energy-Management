class EnergyEnvironment:
    def __init__(
        self,
        pv_maxpower,
        grid_price,
        grid_max_import,

        battery_capacity,
        battery_efficiency,
        battery_soc_min,
        battery_soc_max,
        battery_max_charge_power,
        battery_max_discharge_power,

        ev_capacity,
        ev_soc_min,
        ev_soc_max,
        ev_soc_target,
        ev_max_charge_power,
        ev_arrival_hour,
        ev_departure_hour,

        solar_data,
        load_data
    ):

        self.pv_maxpower = pv_maxpower

        self.grid_price = grid_price
        self.grid_max_import = grid_max_import
        
        self.battery_capacity = battery_capacity
        self.battery_efficiency = battery_efficiency
        self.battery_soc_min = battery_soc_min
        self.battery_soc_max = battery_soc_max
        self.battery_max_charge_power = battery_max_charge_power
        self.battery_max_discharge_power = battery_max_discharge_power

        self.ev_capacity = ev_capacity
        self.ev_soc_min = ev_soc_min
        self.ev_soc_max = ev_soc_max
        self.ev_soc_target = ev_soc_target
        self.ev_max_charge_power = ev_max_charge_power
        self.ev_arrival_hour = ev_arrival_hour
        self.ev_departure_hour = ev_departure_hour

        self.solar_data = solar_data
        self.load_data = load_data

        self.hour = 0
        self.battery_soc = 40
        self.ev_soc = 44

    def reset(self):

        self.hour = 0

        self.battery_soc = 40
        self.ev_soc = 44

        self.solar = self.solar_data[self.hour]
        self.load = self.load_data[self.hour]

        state = [
            self.solar,
            self.load,
            self.battery_soc,
            self.grid_price,
            self.ev_soc,
            self.hour
        ]

        return state

    def step(self, action):

        action[0] = battery_power
        action[1] = ev_charge_power

        grid_import = 0
        ev_charge_power = 0
        battery_power = 0
        rew_ev = 0
        target_rew = 0

        if self.ev_arrival_hour <= self.hour < self.ev_departure_hour:
            if ev_action > 0 and self.ev_soc < self.ev_soc_target:

                ev_stored_energy = (
                    self.ev_soc / 100
                ) * self.ev_capacity

                target_energy = (
                    self.ev_soc_target / 100
                ) * self.ev_capacity

                remaining_capacity = max(
                    0,
                    target_energy - ev_stored_energy
                )

                ev_charge_power = min(
                    ev_action,
                    self.ev_max_charge_power,
                    remaining_capacity
                )

                ev_soc_old = self.ev_soc

                ev_soc_t_next = (
                    (ev_stored_energy + ev_charge_power)
                    / self.ev_capacity
                    * 100
                )

                self.ev_soc = ev_soc_t_next

                rew_ev = 3 * (
                    ev_soc_t_next - ev_soc_old
                )

        battery_stored_energy = (
            self.battery_soc / 100
        ) * self.battery_capacity

        if battery_action > 0:

            remaining_battery_capacity = (
                self.battery_capacity
                * self.battery_soc_max
                / 100
                - battery_stored_energy
            )

            charge = min(
                battery_action,
                self.battery_max_charge_power,
                remaining_battery_capacity
                / self.battery_efficiency
            )

            energy_stored = (
                charge * self.battery_efficiency
            )

            self.battery_soc = (
                (battery_stored_energy + energy_stored)
                / self.battery_capacity
                * 100
            )

            battery_power = charge

        elif battery_action < 0:

            minimum_energy = (
                self.battery_capacity
                * self.battery_soc_min
                / 100
            )

            available_energy = max(
                0,
                battery_stored_energy - minimum_energy
            )

            discharge_power = min(
                abs(battery_action),
                self.battery_max_discharge_power,
                available_energy
                * self.battery_efficiency
            )

            energy_from_battery = (
                discharge_power
                / self.battery_efficiency
            )

            self.battery_soc = (
                (battery_stored_energy - energy_from_battery)
                / self.battery_capacity
                * 100
            )

            battery_power = -discharge_power

        net_demand = (
            self.load_data[self.hour]
            + ev_charge_power
        )

        if battery_power > 0:
            net_demand += battery_power

        elif battery_power < 0:
            net_demand += battery_power

        solar_used = self.solar_data[self.hour]

        grid_import = max(
            0,
            net_demand - solar_used
        )

        grid_violation = (
            grid_import > self.grid_max_import
        )

        grid_import = min(
            grid_import,
            self.grid_max_import
        )

        c1 = 13

        rew_grid = (
            -c1
            * grid_import
            * self.grid_price
        )

        b = 8
        p = -8
        r = 10
        rviolation = 0

        if self.hour == self.ev_departure_hour - 1:

            if self.ev_soc >= self.ev_soc_target:
                target_rew = b
            else:
                target_rew = p

        if (
            self.battery_soc < self.battery_soc_min
            or self.battery_soc > self.battery_soc_max
            or grid_violation
            or self.ev_soc < self.ev_soc_min
            or self.ev_soc > self.ev_soc_max
        ):
            rviolation = r

        rewards = (
            rew_grid
            + rew_ev
            + target_rew
            - rviolation
        )

        self.hour += 1

        done = self.hour >= 24

        if done:

            next_state = [
                self.solar_data[23],
                self.load_data[23],
                self.battery_soc,
                self.grid_price,
                self.ev_soc,
                self.hour
            ]

        else:

            next_state = [
                self.solar_data[self.hour],
                self.load_data[self.hour],
                self.battery_soc,
                self.grid_price,
                self.ev_soc,
                self.hour
            ]

        return rewards, self.hour, done, next_state