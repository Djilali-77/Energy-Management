from environment import EnergyEnvironment


solar_data = [
    2, 3, 4, 5, 6, 7,
    8, 9, 10, 11, 12, 13,
    14, 13, 12, 11, 10, 9,
    8, 7, 6, 5, 2, 1
]

load_data = [
    5, 5, 5, 5, 6, 6,
    6, 7, 7, 8, 8, 9,
    9, 8, 8, 7, 7, 6,
    6, 6, 5, 5, 2, 1
]


env = EnergyEnvironment(
    pv_maxpower=15,

    grid_price=0.20,
    grid_max_import=10,

    battery_capacity=10,
    battery_efficiency=0.90,
    battery_soc_min=20,
    battery_soc_max=90,
    battery_max_charge_power=5,
    battery_max_discharge_power=5,

    ev_capacity=10,
    ev_soc_min=20,
    ev_soc_max=100,
    ev_soc_target=80,
    ev_max_charge_power=3,
    ev_arrival_hour=8,
    ev_departure_hour=18,

    solar_data=solar_data,
    load_data=load_data
)

action = [2.0, 1.0]

reward, hour, done, next_state = env.step(action)


env.reset()

print("Initial:")
print("Hour:", env.hour)
print("Battery SOC:", env.battery_soc)
print("EV SOC:", env.ev_soc)

print("\n--- Simulation ---")

done = False

while not done:

    reward, hour, done, next_state = env.step(action)

    print(
        f"Hour: {hour} | "
        f"Battery: {env.battery_soc:.2f}% | "
        f"EV: {env.ev_soc:.2f}% | "
        f"Reward: {reward:.2f} | "
        f"Done: {done}"
    )

print("\nSimulation finished.")