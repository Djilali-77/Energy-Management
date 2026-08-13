from battery import Battery
from ev import Ev
from grid import Grid
from load import Load
from pv import Solar


pv = Solar(12)
load = Load()
battery = Battery(40)
grid = Grid(2, 10)
ev = Ev(43, 17, 23)

h = 0

while h < 24:

    s = pv.get_production(h)
    l = load.get_demand(h)

    grid_import = 0
    charge_ev = 0
    charge_btr = 0
    discharge_btr = 0

    # CASE 1: PV > Load
    if s > l:
        surplus = s - l
        # 1. EV first
        charge_ev = ev.charge(h, surplus)
        # 2. Remaining solar surplus -> Battery
        remaining_surplus = surplus - charge_ev
        if remaining_surplus > 0:
            charge_btr = battery.charge(
                remaining_surplus,
                0
            )
        # No Grid needed
        grid_import = 0

    # CASE 2: PV < Load
    else:
        deficit = l - s
        # 1. Battery supplies the deficit
        discharge_btr = battery.discharge(s, l)
        # 2. Remaining deficit -> Grid
        remaining_deficit = max(
            0,
            deficit - discharge_btr
        )
        # EV charging from Grid
        if ev.arrival_hour <= h < ev.departure_hour:
            # Max Grid power available
            remaining_grid_capacity = (
                grid.max_import - remaining_deficit
            )
            if remaining_grid_capacity > 0:
                charge_ev = ev.charge(
                    h,
                    remaining_grid_capacity
                )
                grid_import = (
                    remaining_deficit + charge_ev
                )
            else:
                grid_import = remaining_deficit
        else:
            grid_import = remaining_deficit
        # Respect Grid maximum import
        grid_import = min(
            grid_import,
            grid.max_import
        )
    # Grid cost
    cost = grid.calcule_cost(grid_import)


    # Results
    print(
        f"Hour: {h:02d} | "
        f"Solar: {s:5.2f} kW | "
        f"Load: {l:5.2f} kW | "
        f"EV SOC: {ev.soc:5.1f}% | "
        f"Battery SOC: {battery.soc:5.1f}% | "
        f"EV Charge: {charge_ev:4.2f} kW | "
        f"Battery Charge: {charge_btr:4.2f} kW | "
        f"Battery Discharge: {discharge_btr:4.2f} kW | "
        f"Grid: {grid_import:5.2f} kW | "
        f"Cost: {cost:5.2f}"
    )

    h += 1