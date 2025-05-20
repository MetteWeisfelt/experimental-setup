from strategies.Strategy import Strategy
from sklearn.linear_model import SGDClassifier
import numpy as np


class SGDClassifierTradingStrategy(Strategy):
    def __init__(self, window_size=50):
        super().__init__()
        self.window_size = window_size
        self.model = SGDClassifier(loss='hinge')
        self.correct_guesses = np.array([])

    def place_bet(self):
        if len(self.observed_values) < self.window_size:
            return 0

        self.incremental_train()

        X = np.array(self.observed_values[-self.window_size:]).reshape(1, -1)
        prediction = self.model.predict(X)[0]

        return prediction

    def incremental_train(self):
        if len(self.observed_values) >= self.window_size:
            X = np.array(self.observed_values[-self.window_size:]).reshape(1, -1)
            y = [1 if self.observed_values[-1] > self.observed_values[-2] else 0]

            if not hasattr(self.model, 'classes_'):
                self.model.partial_fit(X, y, classes=[0, 1])
            else:
                self.model.partial_fit(X, y)

    def reset(self):
        super().reset()
        self.model = SGDClassifier(loss='hinge', random_state=42)
        self.correct_guesses = np.array([])