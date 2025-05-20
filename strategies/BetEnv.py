from typing import Optional, Union, List

import gym
from gym.core import RenderFrame
from gym.spaces import Discrete, Box
import numpy as np


class BetEnv(gym.Env):
    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        pass

    def __init__(self, config):
        self.generator = config["generator"]
        self.history_size = config.get("history_size", 1)
        self.max_steps = config.get("max_steps", 10000)
        self.step_count = 0

        self.action_space = Discrete(2)  # 0 = guess next is lower or same, 1 = guess higher
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(self.history_size,), dtype=np.float32)

        self.history = []

    def reset(self):
        self.generator.reset()
        self.step_count = 0
        self.history = [self.generator.generate() for _ in range(self.history_size)]
        return np.array(self.history, dtype=np.float32)

    def step(self, action):
        prev = self.history[-1]
        next_val = self.generator.generate()

        correct = int(next_val > prev)
        reward = 1.0 if action == correct else -1.0

        self.history.pop(0)
        self.history.append(next_val)

        self.step_count += 1
        done = self.step_count >= self.max_steps

        return np.array(self.history, dtype=np.float32), reward, done, {}
