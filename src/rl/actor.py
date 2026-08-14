import torch
import torch.nn as nn
from torch.distributions import Normal

class Actor(nn.Module):

    def __init__(self, state_dim = 6, action_dim = 2):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh()
        )

        self.mean = nn.Linear(64, 2)

        self.log_std = nn.Parameter(
            torch.zeros(action_dim)
        )

    def forward(self, state):
        
        x = self.network(state)
        mean = self.mean(x)
        std = torch.exp(self.log_std)
        distribution = Normal(mean, std)

        return distribution

    def get_action(self, state):

        distribution = self.forward(state)
        action = distribution.sample()
        log_prob = distribution.log_prob(action).sum(dim=-1)

        return action, log_prob

actor = Actor()
state = torch.tensor(
    [500, 300, 40, 13, 44, 0],
    dtype=torch.float32
)

action, log_prob = actor.get_action(state)
