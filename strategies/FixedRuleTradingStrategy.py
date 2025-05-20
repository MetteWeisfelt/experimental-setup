from strategies.Strategy import Strategy


class FixedRuleTradingStrategy(Strategy):
    def place_bet(self):
        previous = self.observed_values[self.observed_values.size - 1]
        previous_previous = self.observed_values[self.observed_values.size - 2]

        if previous >= previous_previous:
            return 1
        else:
            return 0
