from strategies.Strategy import Strategy
import numpy as np


class MeanReversionFullTradingStrategy(Strategy):
    def place_bet(self):
        mean = np.sum(self.observed_values) / len(self.observed_values)
        last_observed = self.get_last_observed_value()

        if last_observed < mean:
            return 1
        else:
            return 0
