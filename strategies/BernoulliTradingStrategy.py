from strategies.Strategy import Strategy


class BernoulliTradingStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.higher_count = 0
        self.lower_count = 0
        self.last_value = None

    def observe(self, value):
        super().observe(value)
        if self.last_value is not None:
            if value > self.last_value:
                self.higher_count += 1
            elif value < self.last_value:
                self.lower_count += 1
        self.last_value = value

    def place_bet(self):
        if self.higher_count < self.lower_count:
            return 0
        else:
            return 1

    def reset(self):
        super().reset()
        self.higher_count = 0
        self.lower_count = 0
        self.last_value = None
