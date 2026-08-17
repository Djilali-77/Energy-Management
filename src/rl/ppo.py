import torch

from environment import EnergyEnvironment
from actor import Actor
from critic import Critic


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


def compute_gae(rewards, values, dones, gamma=0.99, lam=0.95):

    advantages = []
    gae = 0

    for t in reversed(range(len(rewards))):

        if t == len(rewards) - 1:
            next_value = 0
        else:
            next_value = values[t + 1]

        delta = (
            rewards[t]
            + gamma * next_value * (1 - dones[t])
            - values[t]
        )

        gae = (
            delta
            + gamma * lam * (1 - dones[t]) * gae
        )

        advantages.insert(0, gae)

    return torch.stack(advantages)


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


actor = Actor()
critic = Critic()


actor_optimizer = torch.optim.Adam(
    actor.parameters(),
    lr=3e-4
)

critic_optimizer = torch.optim.Adam(
    critic.parameters(),
    lr=1e-3
)


states = []
actions = []
log_probs = []
rewards = []
values = []
dones = []


state = env.reset()
done = False


while not done:

    state_tensor = torch.tensor(
        state,
        dtype=torch.float32
    )

    action, log_prob = actor.get_action(
        state_tensor
    )

    value = critic(state_tensor)

    reward, hour, done, next_state = env.step(
        action.detach().numpy()
    )

    states.append(state)
    actions.append(action.detach())
    log_probs.append(log_prob.detach())
    rewards.append(reward)
    values.append(value.detach())
    dones.append(done)

    state = next_state


advantages = compute_gae(
    rewards,
    values,
    dones
)

returns = advantages + torch.stack(values)


states_tensor = torch.stack([
    torch.tensor(
        s,
        dtype=torch.float32
    )
    for s in states
])

actions_tensor = torch.stack(actions)

old_log_probs_tensor = torch.stack(
    log_probs
).squeeze(-1)

advantages_tensor = advantages.detach()


distribution = actor(states_tensor)

new_log_probs = distribution.log_prob(
    actions_tensor
).sum(dim=-1)


ratio = torch.exp(
    new_log_probs - old_log_probs_tensor
)


clip_eps = 0.2

clipped_ratio = torch.clamp(
    ratio,
    1 - clip_eps,
    1 + clip_eps
)


actor_loss = -torch.min(
    ratio * advantages_tensor,
    clipped_ratio * advantages_tensor
).mean()


values_tensor = torch.stack(
    values
).squeeze(-1)

returns_tensor = returns.detach().squeeze(-1)


critic_loss = (
    returns_tensor - values_tensor
).pow(2).mean()


actor_optimizer.zero_grad()

actor_loss.backward()

actor_optimizer.step()


critic_optimizer.zero_grad()

critic_loss.backward()

critic_optimizer.step()


print("States:", len(states))
print("Actions:", len(actions))
print("Rewards:", len(rewards))
print("Actor Loss:", actor_loss.item())
print("Critic Loss:", critic_loss.item())
print("Advantages:", advantages)
print("Returns:", returns)