from strategies.Strategy import Strategy
import numpy as np


class MeanReversionTimeWindowedTradingStrategy(Strategy):
    def __init__(self, time_window):
        super().__init__()
        self.time_window = time_window

    def place_bet(self):
        mean = np.sum(self.get_last_time_window_observed_values(self.time_window)) / self.time_window
        last_observed = self.get_last_observed_value()

        if last_observed < mean:
            return 1
        else:
            return 0
