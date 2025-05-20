from generators.Generator import Generator
import numpy as np


class SineWaveGenerator(Generator):
    def change_parameters_after_warmup(self):
        self.__class__.step_size = 0.2

    step_size = 0.1

    def __init__(self):
        self.w_previous = 0
        self.w_current = np.sin(self.__class__.step_size)
        self.cos_delta = 2 * np.cos(self.__class__.step_size)
        self.counter = 0

    def reset(self):
        self.w_previous = 0
        self.w_current = np.sin(self.__class__.step_size)
        self.cos_delta = 2 * np.cos(self.__class__.step_size)
        self.counter = 0

    def generate(self):
        if self.counter == 0:
            self.counter += 1
            return self.w_current

        # recalibrate every 3500 steps to prevent numerical drift
        if self.counter % 3500 == 0:
            self.w_current = np.sin(self.counter * self.__class__.step_size)
            self.w_previous = np.sin((self.counter - 1) * self.__class__.step_size)
        else:
            w_next = self.cos_delta * self.w_current - self.w_previous
            self.w_previous, self.w_current = self.w_current, w_next

        self.counter += 1
        return self.w_current
