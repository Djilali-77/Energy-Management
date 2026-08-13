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
while( h < 24):

    s = pv.get_production(h)
    l = load.get_demand(h)
    if s > l:
        
        charge_ev = ev.charge(h, (s - l))
        remaining_surplus = (s - l) - charge_ev
        charge_btr = battery.charge(remaining_surplus, 0)
        grid_import = 0
    else:
        discharge_btr = battery.discharge(s, l)
        grid_import = max(0, l - s - discharge_btr)

    cost = grid.calcule_cost(grid_import)

    print(
        f"Hour: {h:02d} | "
        f"Solar: {s:5.2f} kW | "
        f"Load: {l:5.2f} kW | "
        f"EV SOC: {ev.soc:5.1f}% | "
        f"Battery SOC: {battery.soc:5.1f}% | "
        f"Grid: {grid_import:5.2f} kW | "
        f"Cost: {cost:5.2f}"
    )

    h += 1
