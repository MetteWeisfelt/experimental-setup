import numpy as np
import matplotlib.pyplot as plt


class WarmupGame:
    def __init__(self, generator, observer, total_movements, start_value=0):
        self.generator = generator
        self.observer = observer
        self.total_movements = total_movements
        self.previous_movement = start_value
        self.score = 0
        self.score_development = np.array([])
        self.total_correct_bets = 0
        self.total_incorrect_bets = 0
        self.bet_results = []
        self.warmup_period = 8000

    def play_turn(self):
        value = self.generator.generate()
        bet = self.observer.place_bet()

        correct_bet = int(
            (value > self.previous_movement and bet == 1) or (value < self.previous_movement and bet == 0))

        self.bet_results.append((value, bet, bool(correct_bet)))

        if correct_bet == 1:
            self.total_correct_bets += 1
        else:
            self.total_incorrect_bets += 1

        if value < self.previous_movement and bet == 0:
            self.score += 1
        elif value > self.previous_movement and bet == 1:
            self.score += 1
        elif value > self.previous_movement and bet == 0:
            self.score -= 1
        elif value < self.previous_movement and bet == 1:
            self.score -= 1

        self.previous_movement = value
        self.score_development = np.append(self.score_development, self.score)

    def play_game(self):
        for i in range(self.total_movements):
            if i == self.warmup_period:
                self.generator.update_parameters_after_warmup()

            self.observer.observe(self.previous_movement)
            self.play_turn()

        return self.score


