from ray.rllib import SampleBatch
from ray.util.client import ray

from strategies.BetEnv import BetEnv
from strategies.Strategy import Strategy
import numpy as np
from ray.rllib.agents.ppo import PPOTrainer


class ReinforcementLearningTradingStrategy(Strategy):
    def __init__(self, generator, history_size=1):
        self.history_size = history_size
        self.generator = generator

        ray.init(ignore_reinit_error=True)

        # Register env for rllib
        def env_creator(env_config):
            return BetEnv(env_config)

        from ray.tune.registry import register_env
        register_env("StreamingSequenceGuessEnv", env_creator)

        config = {
            "env": "StreamingSequenceGuessEnv",
            "env_config": {
                "generator": self.generator,
                "history_size": self.history_size,
                "max_steps": 10000,
            },
            "framework": "torch",
            "num_workers": 0,
            "lr": 1e-3,
        }
        self.trainer = PPOTrainer(config=config)
        self.policy = self.trainer.get_policy()
        self.observation = [self.generator.generate() for _ in range(self.history_size)]

    def observe(self, value):
        self.observation.append(value)
        if len(self.observation) > self.history_size:
            self.observation.pop(0)

    def place_bet(self):
        if len(self.observation) < self.history_size:
            return np.random.randint(0, 2)
        obs = np.array(self.observation[-self.history_size:], dtype=np.float32)
        action, _, _ = self.policy.compute_single_action(obs)
        return int(action)

    def train_on_step(self, action, reward, next_obs):
        batch = {
            SampleBatch.CUR_OBS: np.array([self.observation], dtype=np.float32),
            SampleBatch.ACTIONS: np.array([action]),
            SampleBatch.REWARDS: np.array([reward], dtype=np.float32),
            SampleBatch.NEXT_OBS: np.array([next_obs], dtype=np.float32),
            SampleBatch.DONES: np.array([False], dtype=bool),
        }
        self.policy.learn_on_batch(batch)
        self.observe(next_obs)
