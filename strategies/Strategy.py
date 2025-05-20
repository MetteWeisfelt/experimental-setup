from abc import ABC, abstractmethod
import numpy as np


class Strategy(ABC):
    @abstractmethod
    def place_bet(self):
        pass

    def __init__(self):
        self.observed_values = np.array([])

    def observe(self, value):
        self.observed_values = np.append(self.observed_values, value)

    def get_frequency_lower(self):
        lower = 0

        for i in range(len(self.observed_values) - 1):
            if self.observed_values[i] > self.observed_values[i + 1]:
                lower += 1

        return lower

    def get_frequency_higher(self):
        higher = 0

        for i in range(len(self.observed_values) - 1):
            if self.observed_values[i] < self.observed_values[i + 1]:
                higher += 1

        return higher

    def get_last_observed_value(self):
        if self.observed_values.size == 0:
            return 0

        return self.observed_values[self.observed_values.size - 1]

    def get_last_movement(self):
        first = self.observed_values[self.observed_values.size - 2]
        second = self.observed_values[self.observed_values.size - 1]

        if first > second:
            return 0
        else:
            return 1

    def get_last_time_window_observed_values(self, time_window):
        return self.observed_values[-time_window:]

    def reset(self):
        self.observed_values = np.array([])
