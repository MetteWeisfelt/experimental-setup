import numpy as np
from strategies.ReinforcementLearningTradingStrategy import ReinforcementLearningTradingStrategy
import matplotlib.pyplot as plt


class Game:
    def __init__(self, generator, total_movements=10000, history_size=1):
        self.generator = generator
        self.total_movements = total_movements
        self.history_size = history_size
        self.rl_model = ReinforcementLearningTradingStrategy()
        self.previous_movement = self.generator.generate()
        self.score = 0
        self.score_development = np.array([])
        self.total_correct_bets = 0
        self.total_incorrect_bets = 0
        self.bet_results = []

        self.rl_model.observe(self.previous_movement)

    def play_turn(self):
        bet = self.rl_model.place_bet()
        next_value = self.generator.generate()

        correct_bet = int(
            (next_value > self.previous_movement and bet == 1) or (next_value < self.previous_movement and bet == 0)
        )

        reward = 1 if correct_bet else -1

        self.bet_results.append((next_value, bet, bool(correct_bet)))
        if correct_bet:
            self.total_correct_bets += 1
            self.score += 1
        else:
            self.total_incorrect_bets += 1
            self.score -= 1

        next_obs = np.array(self.rl_model.observation[-self.history_size:], dtype=np.float32)

        # train on this one step (action, reward, next observation)
        self.rl_model.train_on_step(bet, reward, next_obs)

        self.previous_movement = next_value
        self.score_development = np.append(self.score_development, self.score)

    def play_game(self):
        for _ in range(self.total_movements):
            self.play_turn()
        return self.score
