from generators.Generator import Generator

import yfinance as yf
import numpy as np


class RealWorldAssetPriceGenerator(Generator):
    def change_parameters_after_warmup(self):
        pass

    def __init__(self):
        ticker = 'AAPL'
        self.startValue = 0
        self.data = yf.download(ticker, start="2000-01-01", end="2024-01-01")
        self.open_close_data = self.data[['Open', 'Close']].values.ravel()

    def generate(self):
        if self.startValue >= len(self.open_close_data):
            print(len(self.open_close_data))
            raise StopIteration("no more data")

        generated = self.open_close_data[self.startValue]
        self.startValue += 1
        return generated

    def reset(self):
        self.startValue = 0
