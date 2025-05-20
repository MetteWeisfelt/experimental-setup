from strategies.Strategy import Strategy


class ZeroTradingStrategy(Strategy):
    def place_bet(self):
        return 1
